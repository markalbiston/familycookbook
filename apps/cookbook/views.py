from django.shortcuts import render, redirect
from apps.login.models import User
from apps.cookbook.models import *

def userpage(request, user_id):
    if "user_id" not in request.session:
        # print("is this where i'm breaking down?"*100)
        return redirect('/loginpage')
    user = User.objects.get(id=user_id)
    user_recipes = Recipe.objects.filter(user=user).order_by("title")
    
    # print({user})
    context = {
        "all_categories" : Category.objects.all().order_by("title"),
        "user_categories" : Category.objects.filter(recipe__in=user_recipes).values_list('title',flat=True).distinct().order_by("title"),
        "user_recipes" : user_recipes,
        "current_user" : User.objects.get(id=user_id),
        "user_families" : Family.objects.filter(member=user).order_by("family_name"),
        "all_families" : Family.objects.all().order_by("family_name"),
        "all_comments" : Comment.objects.filter(recipe__in=user_recipes).distinct().order_by("-created_at"),
    }
    return render(request, "cookbook/userpage.html", context)

def gotofamilypage(request, user_id):
    if "user_id" not in request.session:
        return redirect('/loginpage')
    # print(f"{request.POST['family']}")
    if request.method == "POST":
        if request.POST['family'].isdigit():
            family_id = request.POST['family']
            # print(family_id*100)
            return redirect(f"/cookbook/{user_id}/{family_id}")
        else:
            family_name = request.POST['family']
            user = User.objects.get(id=request.session['user_id'])
            this_family = Family.objects.create(family_name=family_name)
            Family.objects.get(family_name=family_name).member.add(user)
            family_id = this_family.id
            # new_family = Family.objects.filter(family_name=family_name)
            # family_name = new_family.family_name
            return redirect(f"/cookbook/{user_id}/{family_id}")

def joinfamily(request, user_id):
    if "user_id" not in request.session:
        return redirect('/loginpage')
    if request.method == "POST":
        family_id = request.POST['joinfamily']
        user = User.objects.get(id=request.session['user_id'])
        Family.objects.get(id=family_id).member.add(user)
        return redirect(f"/cookbook/{user_id}/{family_id}")

def familypage(request, user_id, family_id):
    this_family = Family.objects.get(id=family_id)
    family_members = Family.objects.get(id=family_id).member.all().order_by("first_name")
    family_recipes = Recipe.objects.filter(user__in=family_members).order_by("title")
    family_messages = Message.objects.filter(family=this_family).order_by("-created_at")
    # family_recipes =[]
    # for member in family_members:
    #     family_recipes.append(Recipe.objects.filter(user=member).order_by("title"))
    context = {
        "this_family" : this_family,
        "family_name" : this_family.family_name,
        "all_categories" : Category.objects.all().order_by("title"),
        "family_members" : family_members,
        "family_recipes" : family_recipes,
        # "family_recipes" : family_recipes,
        "family_categories" : Category.objects.filter(recipe__in=family_recipes).values_list('title',flat=True).distinct().order_by("title"),
        "family_messages" : family_messages,
        "all_comments" : Comment.objects.filter(recipe__in=family_recipes).distinct().order_by("-created_at"),

    }
    # print("PRINTHERE")
    # print(family_recipes)
    return render(request, "cookbook/familypage.html", context)

def leavefamily(request, family_id):
    if request.method == "POST":
        this_family = Family.objects.get(id=request.POST['leavefamily'])
        logged_user = request.session['user_id']
        this_family.member.remove(logged_user)
        return redirect(f"/cookbook/{request.session['user_id']}")

def postmessage(request, family_id):
    if request.method == "POST":
        newmessage = request.POST['newmessage']
        logged_user = User.objects.get(id=request.session['user_id'])
        this_family = Family.objects.get(id=family_id)
        Message.objects.create(message_text=newmessage,user=logged_user,family=this_family)
        return redirect(f"/cookbook/{request.session['user_id']}/{family_id}")

def deletemessage(request, family_id):
    if request.method == "POST":
        d = Message.objects.get(id=request.POST['message_to_delete'])
        d.delete()
        return redirect(f"/cookbook/{request.session['user_id']}/{family_id}")

def newrecipecard(request, user_id):
    if "user_id" not in request.session:
        return redirect('/loginpage')
    user=User.objects.get(id=user_id)
    user_recipes = Recipe.objects.filter(user=user).order_by("title")
    context = {
        "all_categories": Category.objects.all().order_by("title"),
        "user_categories" : Category.objects.filter(recipe__in=user_recipes).distinct().order_by("title"),
        "user_families" : Family.objects.filter(member=user).order_by("family_name"),
        "all_families" : Family.objects.all(),
    }
    return render(request, "cookbook/addrecipe.html", context)

def addrecipe(request, user_id):
    if "user_id" not in request.session:
        return redirect('/loginpage')
    if request.method == "POST":
        ingredients = request.POST['ingredients']
        directions = request.POST['directions']
        notes = request.POST['notes']
        title = request.POST['title']
        user = User.objects.get(id=request.session['user_id'])
        # print("we are failing right here")
        # print(f"{request.POST['category']}")
        if request.POST['category'].isdigit():
            category = Category.objects.get(id=request.POST['category'])
            Recipe.objects.create(title=title,ingredients=ingredients,directions=directions,notes=notes,user=user,category=category)
        else:
            category = Category.objects.create(title=request.POST['category'])
            Recipe.objects.create(title=title,ingredients=ingredients,directions=directions,notes=notes,user=user,category=category)
        return redirect(f"/cookbook/{user_id}")

def deleterecipe(request, user_id):
    if request.method == "POST":
        this_recipe = Recipe.objects.get(id=request.POST['recipe_to_delete'])
        this_recipe.delete()
        return redirect(f"/cookbook/{user_id}")

def editrecipecard(request, user_id):
    # print(f"{request.POST['recipe_to_edit']}")
    this_recipe = Recipe.objects.get(id=request.POST['recipe_to_edit'])
    # request.session['this_recipe'] = this_recipe
    user=User.objects.get(id=user_id)
    user_recipes = Recipe.objects.filter(user=user).order_by("title")
    context = {
        "all_categories": Category.objects.all().order_by("title"),
        "user_categories" : Category.objects.filter(recipe__in=user_recipes).distinct().order_by("title"),
        "user_families" : Family.objects.filter(member=user).order_by("family_name"),
        "all_families" : Family.objects.all(),
        "this_recipe" : this_recipe,
    }
    # print("is this the spot?"*100)
    return render(request, "cookbook/editrecipe.html", context)

def editrecipe(request, user_id):
    # if "user_id" not in request.session:
    #     return redirect('/loginpage')
    if request.method == "POST":
        ingredients = request.POST['ingredients']
        directions = request.POST['directions']
        notes = request.POST['notes']
        title = request.POST['title']
        # print({request.POST['recipe_to_edit']})
        edit_recipe = Recipe.objects.get(id=request.POST['recipe_to_edit'])
        edit_recipe.ingredients = ingredients
        edit_recipe.directions = directions
        edit_recipe.notes = notes
        edit_recipe.title = title
        edit_recipe.save()
        return redirect(f"/cookbook/{user_id}")

def postcomment(request, recipe_id):
    if request.method == "POST":
        new_comment = request.POST['newcomment']
        logged_user = User.objects.get(id=request.session['user_id'])
        recipe_to_comment = Recipe.objects.get(id=request.POST['recipe_to_comment'])
        Comment.objects.create(comment_text=new_comment,user=logged_user,recipe=recipe_to_comment)
        current_user = User.objects.get(id=request.POST['current_user_id'])
        family_id = request.POST['comment_from']
        if request.POST['comment_from'] == "userpage":
            return redirect(f"/cookbook/{current_user.id}")
        else:
            return redirect(f"/cookbook/{request.session['user_id']}/{family_id}")

# Create your views here.
