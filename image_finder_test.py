from addons import *

while True:
    # Lost focus of the join button means it can't see the full server widget
    this_server_is_currently_full(output=True)
    are_you_human()
    if on_discord():
        print('on_discord')
    else:
        print("not_on_discord")
    time.sleep(1)