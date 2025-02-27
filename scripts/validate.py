#!/usr/bin/python3
import json

from pkl import (
    DumpTypes,
    dump_dataset,
    pkl_is_install,
    pkl_install_force,
)


def validate_duplicate_title(items) -> bool:
    keys = [item['t'] for item in items]
    duplicates = []
    for key in keys:
        if len([item for item in items if key == item['t']]) > 1:
            if key and key not in duplicates:
                print('> Duplicate title found: "{}"'.format(key if key else 'empty'))
                duplicates.append(key)
    return len(duplicates) == 0


if __name__ == '__main__':
    # install pkl if not exist
    if not pkl_is_install():
        pkl_install_force()

    # get dump json
    print('Create dump...')
    result = dump_dataset(DumpTypes.json, quiet=True)
    if not result:
        exit(1)

    results = []
    data = json.loads(result)
    dataset = data['dataset']
    faq = dataset['faq']
    pub = dataset['pub']

    print('Validate duplicate title FAQ...')
    results.append(validate_duplicate_title(faq['en']))
    results.append(validate_duplicate_title(faq['ru']))

    print('Validate duplicate title Publication...')
    results.append(validate_duplicate_title(pub['en']))
    results.append(validate_duplicate_title(pub['ru']))

    if len([item for item in results if not item]) > 0:
        print('Result: validation errors found.')
    else:
        print('Result: validation was successful.')
