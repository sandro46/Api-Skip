from django.db import models, connection
import random
# Create your models here.

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


class RefSource(models.Model):
    """Model of sources
    #39	Внешний источник	РК - ФССП"""

    name = models.TextField(max_length=50)
    description = models.TextField(max_length=500, null=True)

    class Meta:
        verbose_name = "Источники данных"
        verbose_name_plural = "Источники данных"


class Template(models.Model):

    name = models.CharField(max_length=255)
    template = models.TextField()
    creator = models.CharField(max_length=50, null=True)
    created = models.DateTimeField("Дата создания", auto_now_add=True, null=True)
    source = models.ManyToManyField(RefSource, related_name='template_source_rel')

    class Meta:
        verbose_name = "Таблица с шаблонами параметров для поиска"
        verbose_name_plural = "Таблица с шаблонами параметров для поиска"


class FilePackage(models.Model):
    object_id = models.IntegerField("Индентификатор объекта")
    template = models.ForeignKey(Template, verbose_name="Ссылка на шаблон", related_name="fk_template_filepackage",
                                 on_delete=models.CASCADE)

    @staticmethod
    def get_data(template_id):
        cursor = connection.cursor()
        cursor.execute("""	
                        select 
                            fp.object_id,
                            a.last_name||' '||a.first_name||(case when a.middle_name is not null then ' '||a.middle_name else '' end) fio,
                            a.last_name||'|'||a.first_name||(case when a.middle_name is not null then '|'||a.middle_name else '' end)||'|'||to_char(a.birthday, 'dd.mm.yyyy') search_str,
                            to_char(a.birthday, 'dd.mm.yyyy') search_date 
                        from skip.skip_tools_filepackage fp
                        join sys.v_agreement_card a ON a.agreement_id=fp.object_id
                        where fp.template_id=%s
                    """, params=[template_id])
        return cursor

    class Meta:
        verbose_name = "Таблица с id, залитыми из файла"


# class TemplateSourceList(models.Model):
#     """Link template with sources"""
#
#     template = models.ForeignKey(Template, verbose_name="Ссылка на шаблон",
#                                  related_name="fk_tempalte_sourcelist_template", on_delete=models.CASCADE)
#     source = models.ForeignKey(RefSource, verbose_name="Источник", related_name="fk_tempalte_sourcelist_source",
#                                on_delete=models.CASCADE)


class Task(models.Model):

    template = models.ForeignKey(Template, verbose_name="template_link", related_name="fk_template_task", on_delete=models.CASCADE)
    search_type = models.CharField(max_length=50)
    is_ok = models.CharField(max_length=1, default='N')
    prio = models.IntegerField("Приоритет поиска")
    descr = models.CharField(max_length=500, null=True)
    percent_complete = models.IntegerField(default=0)
    start_dt = models.DateTimeField("Дата создания", auto_now_add=True, null=True)
    end_dt = models.DateTimeField("Дата Завершения", null=True)

    class Meta:
        verbose_name = "Задачи на поиск"
        verbose_name_plural = "Задачи на поиск"


class Search(models.Model):
    """Model of skip search log"""

    fio = models.CharField(max_length=50)
    search_str = models.CharField(max_length=50)
    search_date = models.DateTimeField()
    batch_id = models.IntegerField("Индентификатор пачки для многопоточности", null=True)
    task = models.ForeignKey(Task, verbose_name="Блок поиска", related_name="fk_search_task", on_delete=models.CASCADE, null=True)
    person_id = models.IntegerField()
    date_search = models.DateTimeField("Дата поиска", null=True)
    date_parsed = models.DateTimeField("Дата парсинга", null=True)

    @staticmethod
    def getBatch(**kwargs):
        cursor = connection.cursor()

        batch_id = random.randint(0, 99999)
        cursor.execute(
            """with t as (
                SELECT
                    s.*,
                    %s as batch_id1
                FROM skip.skip_tools_search s
                join skip.skip_tools_task task ON task.id=s.task_id
                join skip.skip_tools_template tpl ON tpl.id=task.template_id
                join skip.skip_tools_template_source ts ON ts.template_id=tpl.id
                where refsource_id=%s
                      and s.date_search is null
                      and s.date_parsed is null
                      and batch_id is null
                order by task.prio, task.start_dt
                limit %s
            )
    
            update skip.skip_tools_search s
            SET batch_id = t.batch_id1,
                date_search=current_timestamp
            from t
            where
                t.id = s.id
            RETURNING t. * """, params=[batch_id, kwargs['source_id'], kwargs['limit']]
        )

        return dictfetchall(cursor)

    class Meta:
        verbose_name = "Основная таблица для логирования поиска"
        verbose_name_plural = "Основная таблица для логирования поиска"

class TaskFiles(models.Model):

    name = models.CharField(max_length=255)
    task = models.ForeignKey(Task, verbose_name="Блок поиска", related_name="fk_task_files_task", on_delete=models.CASCADE)
    source = models.ForeignKey(RefSource, verbose_name="Источник", related_name="fk_task_files_source", on_delete=models.CASCADE, null=True)
    created = models.DateTimeField("Дата создания", auto_now_add=True, null=True)
    file_type = models.CharField("Тип файла", max_length=255, null=True)

    class Meta:
        verbose_name = "Файлы, которые прикрепляются к таскам"
        verbose_name_plural = "Файлы, которые прикрепляются к таскам"


class FoundMap(models.Model):

    search = models.ForeignKey(Search, verbose_name="Ссылка на единицу поиска", related_name="fk_found_search", on_delete=models.CASCADE, null=True)
    url = models.TextField("Адрес страницы или другой идентификатор, по которому было что то найдено", unique=True)
    created = models.DateTimeField("Дата создания", auto_now_add=True, null=True)

    class Meta:
        verbose_name = "Карта удачных поисков"


class Result(models.Model):

    found = models.ForeignKey(FoundMap, verbose_name="Ссылка на карту найденных", related_name="fk_result_found", on_delete=models.CASCADE, null=True)
    data_set_num = models.IntegerField("Порядковый номер набора результатов", null=True)
    data_type = models.CharField("Тип ", max_length=255, null=True)
    data_value = models.TextField("Значение", null=True)
    created = models.DateTimeField("Дата создания", auto_now_add=True, null=True)

    class Meta:
        verbose_name = "Результат поиска"


class WebKey(models.Model):
    source = models.ForeignKey(RefSource, verbose_name="Ссылка на источник", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, null=True)
    provider = models.CharField("Название провайдера, предоставившего ключ", max_length=255, null=True)
    status = models.IntegerField("1 - активен, 0 - неактивен", default=1)
    last_used = models.DateTimeField("Дата последнего использования", null=True)
    n_requests = models.IntegerField("Счётчик запросов", null=True)
    proxy_addr = models.CharField(max_length=255, null=True)
    proxy_user = models.CharField(max_length=255, null=True)
    proxy_pass = models.CharField(max_length=255, null=True)
    date_del = models.DateTimeField("Дата удаления", null=True)
    batch_id = models.IntegerField("Индентификатор пачки для многопоточности", null=True)

    class Meta:
        verbose_name = "Логины пользователей, прокси адреса"