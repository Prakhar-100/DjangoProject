from django.shortcuts import render, redirect
from .models import GroupMessage, ChatGroupList, OnetoOneMessage
import datetime
from core.models import CustomUser
from django.http import JsonResponse

# def index(request):
# 	print("here")
# return render(request, 'chat/index.html')

def index(request):
    return render(request,'chat/index.html') 

def room(request, room_name):
    name = request.user.first_name +"  "+ request.user.last_name

    if request.method == 'POST':
    	txt = request.POST['mytext']
    	GroupMessage.objects.create(e_id = request.user.id,
    		                       e_name = name,
    		                       e_message = txt,
    		                       e_time =  datetime.datetime.today().time()
    		                       )

    text_msg = GroupMessage.objects.all()
    context = {'room_name': room_name, 'txtmsg': text_msg}
    return render(request, 'chat/room.html', context)

def display_empname():
    all_members = CustomUser.objects.all()
    PM,Web,CTO,TL,DIR = [],[],[],[],[]
    for member in all_members:
        if member.designation == 'Project Manager':
            PM.append(member)
        elif member.designation == 'Web Developer':
            Web.append(member)
        elif member.designation == 'Cheif Technical Officer':
            CTO.append(member)
        elif member.designation == 'Director':
            DIR.append(member)
        else:
            TL.append(member)
    return {'all_members': all_members,'PM': PM, 'Web':Web,'CTO':CTO, 'DIR':DIR, 'TL': TL}

def create_channel(request):
    context =  display_empname()
    if request.method == "POST":
        l3 = request.POST.getlist('members') + [str(request.user.id)]
        ides = CustomUser.objects.filter(id__in = l3)
        obj2 = ChatGroupList.objects.create(
                                admin_name = request.user.username,
                                group_name = request.POST['grpname'],
                                description = request.POST['description'], 
                                )
        obj2.member_name.set(ides)
        return redirect('user-chat-room')
        # return redirect()
    return render(request, 'chat/create_channel.html', context)

def load_channel_usernames(request):
    """ This function is used to pass the record of the user on ajax request 
      """
    # usernmId = request.GET.get('usernmId')
    choice = []
    dict2 = {}
    queryset = CustomUser.objects.all()
    obj = CustomUser.objects.get(id = request.user.id)
    for i in queryset:
        if obj.designation == 'Project Manager' and i.designation == 'Tech Leader':
            choice.append({"id":i.id, "name":i.username, "designation": i.designation,
                "first_name": i.first_name, "last_name": i.last_name})
        elif obj.designation == 'Director' and i.designation == 'Cheif Technical Officer':
            choice.append({"id":i.id, "name":i.username, "designation": i.designation,
                "first_name": i.first_name, "last_name": i.last_name})
        elif obj.designation == 'Cheif Technical Officer' and i.designation == 'Project Manager':
            choice.append({"id":i.id, "name":i.username, "designation": i.designation,
                "first_name": i.first_name, "last_name": i.last_name})
        elif obj.designation == 'Tech Leader' and i.designation == 'Web Developer':
            choice.append({"id":i.id, "name":i.username, "designation": i.designation,
                "first_name": i.first_name, "last_name": i.last_name})
        elif obj.designation == 'Cheif Technical Officer' and i.designation != 'Director':
            choice.append({"id":i.id, "name":i.username, "designation": i.designation,
                "first_name": i.first_name, "last_name": i.last_name})
    return JsonResponse(choice, safe=False)

def filter_channel_names(request):
    chatlink = ChatGroupList.objects.all()
    mylink, onelink, multilink = [], [], []

    for obj in chatlink:
        if request.user in obj.member_name.all():
            mylink.append(obj)

    for obj1 in mylink:
        if obj1.member_name.all().count() > 2:
            multilink.append(obj1)
        else:
            onelink.append(obj1)
    return onelink, multilink

def group_chat_room(request, id):

    onelink, multilink = filter_channel_names(request)

    message = GroupMessage.objects.filter(e_groupid = id)
    name = request.user.first_name +"  "+ request.user.last_name

    if request.method == "POST":
        txt = request.POST['mytext']
        GroupMessage.objects.create(e_id = request.user.id,
                                    e_name = name,
                                    e_message = txt,
                                    e_time =  datetime.datetime.today().time(),
                                    e_groupid = id
                                   )

    context = {'onelink': onelink, 'multilink': multilink, 'message': message, 'room_name': 'groupchat'}
    return render(request, 'chat/group_chat_room.html', context)

def onetoone_chat_room(request, id):
    onelink, multilink = filter_channel_names(request)

    message = OnetoOneMessage.objects.filter(e_groupid = id)
    name = request.user.first_name +"  "+ request.user.last_name

    if request.method == "POST":
        txt = request.POST['mytext']
        OnetoOneMessage.objects.create(e_id = request.user.id,
                                    e_name = name,
                                    e_message = txt,
                                    e_time =  datetime.datetime.today().time(),
                                    e_groupid = id
                                   )

    context = {'onelink': onelink, 'multilink': multilink, 'message': message, 'room_name': 'onechat'}
    return render(request, 'chat/group_chat_room.html', context)


# def load_channel_data(request):
#     return JsonResponse(choice, safe=False)

def user_chat_room(request):
    onelink, multilink = filter_channel_names(request)

    context = {'onelink': onelink, 'multilink': multilink}
    return render(request, 'chat/user_chat_room.html', context)

def createone_channel(request):
    enames =  display_empname()
    onelink, multilink = filter_channel_names(request)
    if request.method == "POST":
        l3 = request.POST.getlist('members') + [str(request.user.id)]
        ides = CustomUser.objects.filter(id__in = l3)
        obj1 = CustomUser.objects.get(id = l3[0])
        obj2 = ChatGroupList.objects.create(
                                admin_name = request.user.username,
                                group_name = obj1.first_name +"  "+ obj1.last_name,
                                )
        obj2.member_name.set(ides)
        return redirect('user-chat-room')
    mydict = {'onelink': onelink, 'multilink': multilink}
    context =  {**mydict , **enames}
    return render(request, 'chat/onelinkcreate_channel.html', context)



