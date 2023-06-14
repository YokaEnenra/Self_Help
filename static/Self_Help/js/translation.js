function translate(key, language) {
    var translations = {
        'uk': {
            'Create project': 'Створити проект',
            'Cancel': 'Скасувати',
            'New project creation': 'Створення нового проекту',
            'New note creation': 'Створення нової нотатки',
            'Create note': 'Створити нотатку',
            'Delete Confirmation': 'Підтвердження видалення',
            'Delete Project': 'Видалити проект',
            'Delete Note': 'Видалити Нотатку',
            'Project Editing': 'Зміна Проекту',
            'Confirm Changes': 'Підтвердити зміни',
            'User addition': 'Додавання користувача',
            'Add user': 'Додати користувача',
            'Are you sure you want to delete "': 'Ви впевнені що хочете видалити "',
            '" from this project?': '" з цього проекту?',
            'User Deletion' : 'Видалення користувача',
            'Delete user' : 'Видалити користувача',

        },
    };

    if (translations.hasOwnProperty(language) && translations[language].hasOwnProperty(key)) {
        return translations[language][key];
    }


    return key;
}