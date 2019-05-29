from datetime import datetime
import json, csv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from skip_tools.models import Task, Search, Template, FilePackage, RefSource
from skip_tools.serializers import TaskSerialize, SearchSerialize, TemplatesSerialize

# Create your views here.

def decode_utf8(input_iterator):
    for l in input_iterator:
        yield l.decode('utf-8')


class Tasks(APIView):

    def get(self, request):
        obj = Task.objects.all()
        serializer = TaskSerialize(obj, many=True)
        return Response({"payload12": serializer.data})


class Capcha(APIView):
    def post(self, request):
        # req = json.dumps(request.data)
        # print('[i[ Request data is ', request.data)
        print('[i[ Capcha code is ', request.data['capcha_img'])
        return Response({"payload": 'ok'})


class SearchItems(APIView):

    def get(self, request):
        source_id = request.GET.get("source_id")
        limit = request.GET.get("limit")
        items = Search.getBatch(source_id=source_id, limit=limit)
        return Response({"payload": items})


class Templates(APIView):

    def get(self, request):
        obj = Template.objects.all()
        serializer = TemplatesSerialize(obj, many=True)
        return Response({"payload": serializer.data})

    def post(self, request):
        print("[i] Post contains : ", request.data)

        template, created = Template.objects.update_or_create(name=request.data['tplName'], defaults={
                "name": request.data['tplName'],
                "template": json.dumps(request.data['items'], ensure_ascii=False),
                "creator": 'DevTester'
            }
        )
        for item in request.data['items']:
            if item['name'] == 'agreement_id_list':
                FilePackage.objects.filter(template_id=template.id).delete()
                agreement_ids_list = item['value'].split(',')
                if not agreement_ids_list:
                    continue
                agreement_ids_list = [FilePackage(object_id=i, template_id=template.id) for i in agreement_ids_list]
                print('[i] agreement_ids_list is ', agreement_ids_list)
                FilePackage.objects.bulk_create(agreement_ids_list)

            if item['name'] == 'source_id':
                sources = item['value']
                if not sources:
                    return Response({"payload": {'err': "Source list can`t be empty "}}, status=status.HTTP_400_BAD_REQUEST)
                template.source.clear()
                for i in sources:
                    src = RefSource.objects.get(id=i)
                    template.source.add(src)
                print("[i] Result of insert template soureces list : ")

        print("[i] Post update_or_create created is: ", created)
        return Response({"payload": 'ok'}, status=status.HTTP_201_CREATED)

    def delete(self, request):
        print("[i] Delete id is: ", request.data['id'])
        Template.objects.filter(id=request.data['id']).delete()
        return Response({"payload": 'ok'})

    def put(self, request):
        print("[i] Put request.data is: ", request.data)
        print("[i] Put tplName is: ", request.data['tplName'])
        tpl_object = Template.objects.filter(name=request.data['tplName']).first()
        template = tpl_object.template
        template = json.loads(template)

        for item in template:
            # print('[i] Template item from DB is ', item)
            if not item['value']:
                continue
            if item['name'] == 'debt_sum_from':
                debt_sum_from = item['value']
                print('[i] debt_sum_from is ', debt_sum_from)
            if item['name'] == 'num_persons_to':
                num_persons_to = item['value']
                print('[i] num_persons_to is ', num_persons_to)
            if item['name'] == 'prio':
                prio = item['value']
                print('[i] Prio is ', prio)
            if item['name'] == 'search_type':
                search_type = item['value']
                print('[i] Search_type is ', search_type)

        task = Task.objects.create(template_id=tpl_object.id, search_type=search_type, prio=prio)
        task.save()
        file_pack = FilePackage.get_data(template_id=tpl_object.id)
        print('[file_pack] ', file_pack)
        columns = [x.name for x in file_pack.description]
        insert_list = []
        for row in file_pack:
            row = dict(zip(columns, row))
            insert_list.append(
                Search(
                    fio=row['fio'], search_str=row['search_str'],
                    search_date=str(datetime.strptime(row['search_date'], '%d.%m.%Y')), task_id=task.id, person_id=row['object_id']
                )
            )
        search_lst = Search.objects.bulk_create(insert_list)
        print('[i] Search bulk create result is ', search_lst)
        return Response({"payload": 'ok'})


class FilePackages(APIView):
    def post(self, request):
        csv_file = request.FILES['file']

        if csv_file.multiple_chunks():
            return Response({"payload": {'err': "Uploaded file is too big "}}, status=status.HTTP_400_BAD_REQUEST)

        lines = csv_file.read().decode('windows-1251').splitlines()
        ids = []
        for row in lines:
            fields = row.split(";")
            ids.append(fields[0])
        print('[i] String from csv is ', ','.join(ids))
        return Response({"payload": ','.join(ids)})
