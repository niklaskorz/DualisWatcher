import logging
import traceback
from version_recorder import CollectionOfChanges
from ..notification_service import NotificationService
from .shooter import PushbulletShooter
from .formatter import create_full_dualis_diff, create_full_schedule_diff

class PushbulletService(NotificationService):
    def interactively_configure(self):
        do_pushbullet_input = input('Do you want to activate notifications via pushbullet? [y/n]   ')
        while not (do_pushbullet_input == 'y' or do_pushbullet_input == 'n'):
            do_pushbullet_input = input('Unrecognized input. Try again:   ')
        
        if do_pushbullet_input == 'n':
            self.config_helper.remove_property('pushbullet')
        else:
            config_valid = False
            while not config_valid:
                access_token = input('Your pushbullet access token:   ')

                print('Testing pushbullet config...')
                p = PushbulletShooter(access_token)
                config_valid = p.verify()
                if not config_valid:
                    print('Invalid access token. Please try again.')                
                    continue
            
                pushbullet_cfg = {
                    'access_token': access_token
                }
                self.config_helper.set_property('pushbullet', pushbullet_cfg)
    
    def _send_push(self, title: str, body: str) -> bool:
        try:
            pushbullet_cfg = self.config_helper.get_property('pushbullet')
        except ValueError:
            logging.debug('Pushbullet notifications not configured, skipping.')
            return False
        
        try:
            logging.debug('Sending notification with pushbullet...')
            pushbullet_shooter = PushbulletShooter(pushbullet_cfg['access_token'])
            pushbullet_shooter.send_note(title, body)
            pushbullet_shooter.close()
        except:
            error_formatted = traceback.format_exc()
            logging.error('While sending notification:\n%s' % (error_formatted), extra={'exception': e})
            pass  # ignore the exception further up
    
    def notify_about_changes_in_results(self, changes: CollectionOfChanges, course_names: {str: str}, token: str):
        content = create_full_dualis_diff(changes, course_names)
        self._send_push('{} neue Änderungen in den Modulergebnissen!'.format(changes.diff_count), content)

    def notify_about_changes_in_schedule(self, changes: [str], uid: str):
        content = create_full_schedule_diff(changes, uid)
        self._send_push('{} neue Änderungen im Vorlesungsplan!'.format(len(changes)), content)

    def notify_about_error(self, error_description: str):
        self._send_push('Dualis Watcher Fehler', error_description)
