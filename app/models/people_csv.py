from typing import List

def get_csv_header()->List[str]:
    return list(['id', 'Фамилия','Имя','Отчество','Дата рождения','Серия документа','Номер документа','Дата документа','СНИЛС','ИНН','Статус','id задачи'])

def get_field_names() -> List[str]:
    return list(['id', 'family', 'name', 'patronimic_name', 'bdate', 'docser', 'docno', 'docdt', 'snils', 'inn', 'status'])