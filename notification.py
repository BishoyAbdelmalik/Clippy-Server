import winrt.windows.ui.notifications as notifications
import winrt.windows.data.xml.dom as dom


def send_link_toast(link:str)->None:
    #create notifier
    nManager = notifications.ToastNotificationManager
    notifier = nManager.create_toast_notifier()
    #define your notification as string
    tString = f"""
    <toast launch="-m webbrowser -t {link}">
        <visual>
            <binding template='ToastGeneric'>
                <text>Link Recieved</text>
                <text>{link}</text>
            </binding>
        </visual>
        <actions>

            <action
                content="Open Link"
                arguments="-m webbrowser -t {link}"
                activationType="foreground"/>

            <action
                content="Remind me later"
                arguments="action=remindlater&amp;contentId=351"
                activationType="background"/>

        </actions>
    </toast>
    """
    #convert notification to an XmlDocument
    xDoc = dom.XmlDocument()
    xDoc.load_xml(tString)

    #display notification
    notifier.show(notifications.ToastNotification(xDoc))

