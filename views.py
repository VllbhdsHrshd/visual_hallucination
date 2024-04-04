import os
import random
import pandas as pd
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import F
from django.conf import settings
from django.http import FileResponse, Http404

from .forms import *
from .models import *

MAX_NUM_OF_ANNOTATIONS = 2
TOTAL_ANNOTATIONS_FOR_PAY = 1000


def get_text(id):
    df = pd.read_csv(os.path.join(
        settings.STATIC_DIR, 'combined.csv'))
    tweets = df['tweetContentProcessed'].to_list()
    image_urls = df['mediaUrl'].to_list()
    descriptions = df['description'].to_list()
    image_ids = df['image_id'].to_list()
    indexes = list(range(len(descriptions)))
    all_txt = SubmitText.objects.all()
    # print(all_txt)
    for instance in all_txt:
        idx = instance.idx
        iuis = instance.user_ids.split(",")
        if iuis[0] != '':
            ann_uids = [int(i) for i in iuis]
        else:
            return idx, tweets[idx], image_urls[idx], descriptions[idx], image_ids[idx]
        if len(ann_uids) >= MAX_NUM_OF_ANNOTATIONS or id in ann_uids:
            indexes.remove(idx)

    return indexes[0], tweets[indexes[0]], image_urls[indexes[0]], descriptions[indexes[0]], image_ids[indexes[0]]


def index(request):
    user = request.user
    return render(request, 'hallucination_app/index.html', {'user': user})


def hallucination_page(request):
    # id=request.POST.get('userid')
    id = request.user.id
    if not id:
        return redirect("/")

    template_name = 'hallucination_app/hallucination_page.html'

    if request.method == "POST":
        form = textform(request.POST)
        #print('form prevalidation')
        if form.is_valid():

            id = request.user.id
            if id == "None":
                return redirect('index')
            else:
                text_instance = form.save(commit=False)

                user = UserTxt.objects.filter(userid=id)
                if user.exists():
                    print(user[0].annoted_txt+1)
                    if (user[0].annoted_txt+1) % TOTAL_ANNOTATIONS_FOR_PAY == 0:
                        passcode = User.objects.make_random_password(length=20)
                        while AnnotateCode.objects.filter(code=passcode).exists():
                            passcode = User.objects.make_random_password(
                                length=20)
                        AnnotateCode.objects.create(
                            userid=request.user, code=passcode)
                    UserTxt.objects.filter(userid=id).update(
                        annoted_txt=F("annoted_txt") + 1)

                else:
                    UserTxt.objects.create(
                        userid=request.user, annoted_txt=1)

                res = pd.DataFrame({"idx": [int(text_instance.idx)],
                                    "tweet": [str(text_instance.tweet)],
                                    "image_id": [str(text_instance.image_id)],
                                    "description": [str(text_instance.description)],
                                    "type": [str(text_instance.txt_type)],
                                    "degree": [str(text_instance.txt_degree)],
                                    "nature": [str(text_instance.txt_nature)],
                                    "uid": [str(id)]
                                    })
                if os.path.isfile("data.csv"):
                    df = pd.read_csv("data.csv")[
                        ["idx", "tweet", "image_id", "description", "type", "degree", "nature", "uid"]]
                    df = df.append(res, ignore_index=True)
                    df.to_csv("data.csv")
                else:
                    res.to_csv("data.csv")

                all_texts = SubmitText.objects.filter(
                    idx=str(text_instance.idx))
                if all_texts.exists():
                    SubmitText.objects.filter(idx=str(text_instance.idx)).update(
                        user_ids=all_texts[0].user_ids+","+str(id))
                else:
                    text_instance.user_ids = str(id)
                    text_instance.save()

        print(form.errors)

    # return idx, tweets[idx], image_urls[idx], descriptions[idx], image_ids[idx]
    idx, tweet, image_url, desc, image_id = get_text(id)
    # print(text)
    user = UserTxt.objects.filter(userid=id)
    if user.exists():
        user = UserTxt.objects.get(userid=id)
        number = user.annoted_txt
    else:
        number = 0

    form = textform(initial={'idx': idx, 'tweet': tweet, 'image_id': image_id, 'description': desc, 'txt_type': 'not_hallucination',
                    'txt_degree': 'null', 'txt_nature': 'null'})
    return render(request, template_name, {'image_id': image_id, 'image_url': image_url, 'txt_form': form, 'id': id, 'number': number, 'user': request.user})


def show_codes(request):
    id = request.user.id
    if not id:
        return redirect("/")
    codes = AnnotateCode.objects.filter(userid=id)
    return render(request, "hallucination_app/showCodes.html", {"id": id, "codes": codes})


def view_pdf(request):
    try:
        return FileResponse(open('templates/hallucination_app/definitions.pdf', 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        print(os.getcwd())
        raise Http404()
