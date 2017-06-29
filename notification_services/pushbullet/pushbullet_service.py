from notification_services.notification_service import NotificationService

class PushbulletService(NotificationService):
    def interactively_configure(self):
        do_pushbullet_input = input('Do you want to activate notifications via pushbullet? [y/n]   ')
        while not (do_pushbullet_input == 'y' or do_pushbullet_input = 'n')
            do_pushbullet_input = input('Unrecognized input. Try again:   ')
        
        if do_pushbullet_input == 'n':
            self.config_helper.remove_property('pushbullet')
        else:
            print('[The following Inputs are not validated!]')

            config_valid = False
            while not config_valid:
                access_token = input('Your pushbullet access token:   ')

                print('Testing pushbullet config...')
                
