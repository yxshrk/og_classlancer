from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("togglemode", views.togglemode, name="togglemode"),
    path("homepage", views.homepage, name="homepage"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newperson", views.newperson, name="newperson"),
    path("secondprofile", views.secondprofile, name="secondprofile"),
    path("yourprofile", views.yourprofile, name="yourprofile"),
    path("choicepage", views.choicepage, name="choicepage"),
    path("teacherdashboard", views.teacherdashboard, name="teacherdashboard"),
    path("createjob", views.createjob, name="createjob"),
    path("allclasses", views.allclasses, name="allclasses"),
    path("viewclass/<int:class_id>", views.viewclass, name="viewclass"),
    path("addinquiry/<int:class_id>", views.addinquiry, name="addinquiry"),
    path("addtowatchlist/<int:class_id>", views.addtowatchlist, name="addtowatchlist"),
    path("removefromwatchlist/<int:class_id>", views.removefromwatchlist, name="removefromwatchlist"),
    path("addtimeslots/<int:class_id>", views.addtimeslots, name="addtimeslots"),
    path("choosetimeslot/<int:listingid>", views.choosetimeslot, name="choosetimeslot"),
    path("unselecttimeslot/<int:timeslotid>", views.unselecttimeslot, name="unselecttimeslot"),
    path("profile/<str:user>", views.profile, name="profile"),
    path("searchforclasses", views.searchforclasses, name="searchforclasses"),
    path("editprofile", views.editprofile, name="editprofile"),
    path("editclass/<int:class_id>", views.editclass, name="editclass"),
    path("rateteacher/<str:user>", views.rateteacher, name="rateteacher"),
    path("giverating", views.giverating, name="giverating"),
    path("searchreviews", views.searchreviews, name="searchreviews"),
    path("aboutus", views.aboutus, name="aboutus"),
    path("test", views.test, name="test"),
    path("landingpage", views.forgotpasswordlandingpage, name="landingpage"),
    path("forgotpassword", views.forgotpassword, name="forgotpassword"),
    path("resetpassword", views.resetpassword, name="resetpassword"),
    path("addannouncement/<int:class_id>", views.addannouncement, name="addannouncement"),
    path("yourclasses", views.yourclasses, name="yourclasses"),
    path("contacts", views.contacts, name="contacts"),
    path("newcontact", views.newcontact, name="newcontact"),
    path("newmessage/<str:contact>", views.newmessage, name="newmessage"),
    #path("refreshforcontacts/<str:sender>", views.refreshforcontacts, name="refreshforcontacts"),
    path("chatwithcontacts/<str:contact>", views.chatwithcontacts, name="chatwithcontacts"),
    #path("getmessages/<str:contact>", views.getmessages, name="getmessages"),
    #path("replymessages/<int:message_id>", views.replymessages, name="replymessages"),
    path("resolveall", views.resolveall, name="resolveall"),
    path("findcontact", views.findcontact, name="findcontact"),
    path("ignoreuser/<str:usertoignore>", views.ignoreuser, name="ignoreuser"),
    path("viewyournotifs", views.viewyournotifs, name="viewyournotifs"),
    path("resolvenotifs", views.resolvenotifs, name="resolvenotifs"),
    path("findnewcontact", views.findnewcontact, name="findnewcontact"),
    path("toptutors", views.toptutors, name="toptutors")

]
