from dualis_connector.results_handler import extract_course_name_from_result_page
from version_recorder import CollectionOfChanges

def get_deleted_name(el):
    return extract_course_name_from_result_page(el, 'html.parser')

def filter_diff_lines(modified):
    return ['\n'.join([
        line for line in content.split('\n')
        if ('{+' in line and '+}' in line) or ('[-' in line and '-]' in line) 
    ]) for content in modified]

def create_full_dualis_diff(changes: CollectionOfChanges, course_names: {str, str}) -> str:
    blocks = []
    
    if len(changes.added) > 0:
        blocks.append('\n'.join(
            ['Hinzugefügt:'] +
            [course_names[i] for i in changes.added]
        ))

    if len(changes.deleted) > 0:
        blocks.append('\n'.join(
            ['Entfernt:'] +
            [get_deleted_name(changes.deleted[i]) for i in changes.deleted]
        ))

    if len(changes.modified) > 0:
        blocks.append('\n\n'.join(
            ['Verändert:'] +
            [
                course_names[i] + ':' + '\n'.join(filter_diff_lines(changes.modified[i]))
                for i in changes.modified
            ]
        ))
    
    return '\n\n'.join(blocks)

def create_full_schedule_diff(changes: [str], uid: str) -> str:
    content = ''


    
