import obsws_python as obs
import json
import time

client = obs.ReqClient(host='localhost', port=4445, password='123456')

# GetVersion, returns a response object
resp = client.get_version()
# Access it's field as an attribute
print(f"OBS Version: {resp.obs_version}")


def printJsonObject(object):
    """
    Print an object Json
    Args:
        object (Object): Object is wanted to print
    """
    print(json.dumps(object,indent=3))
    
    
def printJsonObjectList(object_list):
    """
    print a object list

    Args:
        object_list (Array<Object>):  Object list is wanted to print
    """
    for object in object_list:
        printJsonObject(object)
        

def get_input_list(kind=None):
    """Get inputs of obs
    Args:
        kind (String, optional): Restrict the array to only inputs of the specified kind. Defaults to None.

    Returns:
       Object : response contain field "inputs" (Array<Object>)
    """
    return client.get_input_list()


def get_input_settings(name):
    """ 
    To create the entire settings object,
    overlay inputSettings over the defaultInputSettings provided by GetInputDefaultSettings

    Args:
        name (String): Name of the input to get the settings of

    Returns:
        Object contain:
            +input_settings(Object): Object of settings for the input
            +input_kind(String):The kind of the input
    """
    payload = {"inputName": name}
    return client.send("GetInputSettings", payload)
    
    
def set_input_settings(name, settings, overlay):
    """
    Sets the settings of an input.

    Args:
        name (String, optional): Name of the input to set the settings of
        settings (Object):
            -attr:
                + playback_behavior(String): ex: "stop_restart"
                + playlist(Array<object>):
                    -item:
                        hidden(bool): video is hidden or not
                        selected(bool):video is sellected 
                        value(string): path to video or source
                + shuffle(bool): playlist is played random or not
        overlay (bool, optional):   True == apply the settings on top of existing ones, 
                                    False == reset the input to its defaults, then apply settings.

    Returns: None
    """
    return client.set_input_settings(name, settings, overlay)



def get_stream_service_settings():
    """
    Gets the current stream service settings (stream destination)

    Returns:
        object:
        - attr:
            + stream_service_type (String): Stream service type, like rtmp_custom or rtmp_common
            + stream_service_settings(Object): Stream service settings
    """
    return client.get_stream_service_settings()



def set_stream_service_settings(ss_type, ss_settings):
    """
    Sets the current stream service settings (stream destination).
    Note: Simple RTMP settings can be set with type rtmp_custom and the settings fields server and key.

    Args:
        ss_type (String): ype of stream service to apply. Example: rtmp_common or rtmp_custom
        ss_settings (Object): Settings to apply to the service
            -attr:
                + bwtest (bool): bandwide test or not
                + key (String): livestream key
                + protocol (String): type of Protocol is using
                + server (String): server host (can set: auto)
                + service (string): livestream service(twitch, youtube, ...)
    """         


def start_stream():
    """
    start livestream on OBS
    """
    client.start_stream()
    
def stop_stream():
    """
    Stop Livestream on OBS
    """
    client.stop_stream()
    
def toggle_stream():
    """
    toggle Livestream on OBS
    """
    client.toggle_stream()
    
    
def main():
    try:
        response  = get_stream_service_settings()
        print(response.stream_service_type)
        print(response.stream_service_settings)
        print("Live Stream is Starting")
        start_stream()
        
        
        print("-"*100)
        print("GET Input Settings:   ")
        response = get_input_settings("mySource")
        print(f"Input Kind: {response.input_kind}")
        print(f"Input Setting:") 
        printJsonObject(response.input_settings)
        
        time.sleep(10)
        
        
        print("-"*100)
        print("SET Input Settings:")
        settings = {
            "playback_behavior": "stop_restart",
            "playlist": [
                {
                    "hidden": False,
                    "selected": True,
                    "value": "C:/Users/NHAN/OneDrive/Desktop/workspace/CMS/mp4_videos/bird.mp4"
                },
                {
                    "hidden": False,
                    "selected": False,
                    "value": "C:/Users/NHAN/OneDrive/Desktop/workspace/CMS/mp4_videos/ship.mp4"
                },
                {
                    "hidden": False,
                    "selected": False,
                    "value": "C:/Users/NHAN/OneDrive/Desktop/workspace/CMS/mp4_videos/horse.mp4"
                },
                {
                    "hidden": False,
                    "selected": False,
                    "value": "C:/Users/NHAN/OneDrive/Desktop/workspace/CMS/mp4_videos/meeting_1.mp4"
                }
            ],
            "shuffle": False
        }
        printJsonObject(settings)
        set_input_settings(name="mySource",settings=settings,overlay=True)
        
        
        
        time.sleep(30)
    except:
        stop_stream()
        print("Live Stream Stopped")
    
    stop_stream()
    print("Live Stream Stopped")
    
    
    
def startup_test():
    print("-"*100)
    print("SET Input Settings:")
    settings = {
        "playback_behavior": "stop_restart",
        "playlist": [
            {
                "hidden": False,
                "selected": True,
                "value": "C:/Users/NHAN/OneDrive/Desktop/workspace/CMS/mp4_videos/bird.mp4"
            },
            {
                "hidden": False,
                "selected": False,
                "value": "C:/Users/NHAN/OneDrive/Desktop/workspace/CMS/mp4_videos/ship.mp4"
            },
            {
                "hidden": False,
                "selected": False,
                "value": "C:/Users/NHAN/OneDrive/Desktop/workspace/CMS/mp4_videos/horse.mp4"
            }
        ],
        "shuffle": False
    }
    printJsonObject(settings)
    set_input_settings(name="mySource",settings=settings,overlay=True)



def stream_three_video_loopback():
    print("-"*100)
    print("SET Input Settings:")
    settings = {
        "playback_behavior": "stop_restart",
        "playlist": [
            {
                "hidden": False,
                "selected": True,
                "value": "C:/Users/NHAN/OneDrive/Desktop/workspace/CMS/mp4_videos/meeting_1.mp4"
            },
            {
                "hidden": False,
                "selected": False,
                "value": "C:/Users/NHAN/OneDrive/Desktop/workspace/CMS/mp4_videos/ship.mp4"
            },
            {
                "hidden": False,
                "selected": False,
                "value": "C:/Users/NHAN/OneDrive/Desktop/workspace/CMS/mp4_videos/horse.mp4"
            }
        ],
        "shuffle": False
    }
    printJsonObject(settings)
    set_input_settings(name="mySource",settings=settings,overlay=True)

    
    
if __name__ == "__main__":
    stream_three_video_loopback()
    # start_stream()
    # while True:
    #     try:
    #         time.sleep(1)
    #     except KeyboardInterrupt:
    #         # stop_stream()
    #         time.sleep(10)
    #         break
    
    
    
    