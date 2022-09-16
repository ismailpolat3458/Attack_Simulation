# Create your views here.

# Create your views here.


from django.http import HttpResponse
from windows_based_ttp import common
from ttp.tests import ersin



def vss(request):


    common.log("Deleting volume shadow copies...")

    #test_1 = common.execute(["runas", "/noprofile", "vssadmin.exe", "delete", "shadows", "/for=c:", "/oldest", "/quiet"]) #modules.common.execute(["ipconfig"])
    #test_2= common.execute(["wmic.exe", "shadowcopy", "delete", "/nointeractive"])
    test_4= common.execute(["ipconfig"])


    test_3 = " Name: AT Command Lateral Movement " \
             "RTA: at_command.py" \
             "ATT&CK: T1053" \
             "Description: Enumerates at tasks on target host, and schedules an at job for one hour in the future." \
             "Then checks the status of that task, and deletes the task."

    return HttpResponse( ersin("a           ","b","c"))










