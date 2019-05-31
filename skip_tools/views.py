import json, requests, time
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from skip_tools.models import Task, Search, Template, FilePackage, RefSource, Result, FoundMap
from skip_tools.serializers import TaskSerialize, SearchSerialize, TemplatesSerialize
from django.db.models.functions import Now

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
        try:
            capcha = request.data['capcha_img']
        except KeyError:
            return Response({"payload": {'err': "capcha_img can`t be empty "}}, status=status.HTTP_400_BAD_REQUEST)
        params = {
            'key': '2df8c426d6637dc8969b5a5d5255991b',
            'method': 'base64',
            'phrase': 0,
            'regsense': 0,
            'numeric': 4,
            'min_len': 5,
            'max_len': 5,
            'language': 1,
            'json': 1,
            'body': capcha
        }
        response = requests.post("http://rucaptcha.com/in.php", params)
        res = response.json()
        print('[i] Respone1 of recognize capcha is ', res)
        failed = True
        params = {
            'key': '2df8c426d6637dc8969b5a5d5255991b',
            'action': 'get',
            'json': 1,
            'id': res['request']
        }
        for i in range(7):
            time.sleep(5)
            response = requests.get("http://rucaptcha.com/res.php", params)
            assert response.status_code == 200
            if response.status_code == 200:
                res = response.json()
                print('[i] Response capcha result is', res)
                if res['status'] == 1:
                    failed = False
                    break
        if failed:
            return Response({"payload": {'err': "Can`t recognize capcha "}}, status=status.HTTP_404_NOT_FOUND)
        print('[i] Respone2 of recognize capcha is ', res)
        return Response({"payload": res['request']})


class SearchItems(APIView):

    def get(self, request):
        source_id = request.GET.get("source_id")
        limit = request.GET.get("limit")
        items = Search.getBatch(source_id=source_id, limit=limit)
        return Response({"payload": items})

    def post(self, request):
        req = request.data
        print('[i] Search Items Post contains id is: ', req['id'])
        search_item = Search.objects.filter(id=req['id']).first()
        fm = FoundMap.objects.create(search=search_item, url=req['requestUrl'])
        fm.save()
        if 'data' in req:
            insert_list = []
            i = 1
            for row in req['data']:
                print('[i]Row in data is ', row)
                for key in row:
                    insert_list.append(
                        Result(found=fm, data_set_num=i, data_type=key, data_value=row[key])
                    )
                i += 1
            result_list = Result.objects.bulk_create(insert_list)
            print('[i] Result bulk create result is ', result_list)
        search_item.date_parsed = Now()
        search_item.save()
        return Response({"payload": 'ok'})


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
