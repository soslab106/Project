from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from django.http import JsonResponse
from .models import LikeCount, LikeRecord
# Create your views here.

def SuccessResponse(liked_num):
    data = {}
    data['status'] = 'SUCCESS'
    data['liked_num'] = liked_num
    return JsonResponse(data)

def ErrorResponse(code, message):
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)

def like_change(request):
    # 獲取數據
    user = request.user
    if not user.is_authenticated:
        return ErrorResponse(400, '請先登入或註冊!')

    content_type = request.GET.get('content_type')
    object_id = int(request.GET.get('object_id'))

    try:
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return ErrorResponse(401, 'object not exist')

    # 處理數據
    if request.GET.get('is_like') == 'true':
        # 點讚
        like_record, created = LikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)
        if created:
            # 未點過讚，進行點讚
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            like_count.liked_num += 1
            like_count.save()
            return SuccessResponse(like_count.liked_num)
        else:
            # 已點過讚，不能重複點讚
            return ErrorResponse(402, 'you were liked')
    else:
        # 要取消點讚
        if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
            # 有點過讚，取消點讚
            like_record = LikeRecord.objects.get(content_type=content_type, object_id=object_id, user=user)
            like_record.delete()
            # 讚數-1
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            if not created:
                like_count.liked_num -= 1
                like_count.save()
                return SuccessResponse(like_count.liked_num)
            else:
                return ErrorResponse(404, 'data error')
        else:
            # 没有點讚過，不能取消
            return ErrorResponse(403, 'you were not liked')

