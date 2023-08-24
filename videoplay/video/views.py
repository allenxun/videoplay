import re
import os
import mimetypes
from wsgiref.util import FileWrapper
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.conf import settings


from .models import Video, VideoInfo

def index(request):
    result = VideoInfo.objects.all()
    videos = []
    for video in result:
        temp = {}
        temp['id'] = video.id
        temp['name'] = video.name
        temp['season'] = video.season
        temp['episode'] = video.episode
        videos.append(temp)

    # temp = VideoInfo()
    # temp.name = 'test001'
    # temp.season = '10'
    # temp.episode = '12'
    # temp.save()

    return render(request, 'index/index.html', {'videos': videos})

def videoinfo(request,id):
    result = Video.objects.filter(videoId=id)

    videos = []
    for video in result:
        temp = {}
        temp['id'] = video.id
        temp['name'] = video.name
        temp['season'] = video.season
        temp['episode'] = video.episode
        temp['path'] = video.path
        videos.append(temp)
    
    # temp = Video()
    # temp.name = 'test001'
    # temp.videoId = VideoInfo.objects.get(id=id)
    # temp.season = '1'
    # temp.episode = '2'
    # temp.path = '/tmp/'+temp.name+'/'+temp.season+'/'+temp.episode+'.mp4'
    # temp.save()

    return render(request, 'index/videoinfo.html', {'videos': videos})


def file_iterator(file_name, chunk_size=8192, offset=0, length=None):
	# 每次最多读取8Kb
    with open(file_name, "rb") as f:
        f.seek(offset, os.SEEK_SET)
        remaining = length  # 还有多少未读取
        while True:
            bytes_length = chunk_size if remaining is None else min(remaining, chunk_size)
            data = f.read(bytes_length)
            if not data:  # 没有数据了 退出
                break
            if remaining:
                remaining -= len(data)
            yield data


def videoplay(request,id):
    """将视频文件以流媒体的方式响应"""
    range_header = request.META.get('HTTP_RANGE', '').strip()
    range_re = re.compile(r'bytes\s*=\s*(?P<START>\d+)\s*-\s*(?P<END>\d*)', re.I)
    range_match = range_re.match(range_header)
    path = request.GET.get('path')
  #这里根据实际情况改变，我的views.py在core文件夹下但是folder_path却只到core的上一层，media也在core文件夹下
    file_path = Video.objects.get(id=id).path
    
    #video_path = os.path.join(settings.BASE_DIR, 'static', 'video')  # 视频放在目录的static下的video文件夹中
    #ile_path = os.path.join(video_path, path) #path就是template ?path=后面的参数的值


    size = os.path.getsize(file_path)  # 文件总大小
    content_type, encoding = mimetypes.guess_type(file_path)
    content_type = content_type or 'application/octet-stream'
    if range_match:
    	# first_byte播放到的位置
    	# 下次播放的位置 
        first_byte, last_byte = range_match.group('START'), range_match.group('END')
        first_byte = int(first_byte) if first_byte else 0
        # 从播放的位置往后读取10M的数据
        last_byte = first_byte + 1024 * 1024 * 10
        if last_byte >= size:  # 如果想读取的位置大于文件大小
            last_byte = size - 1  # 最后将图片全部读完
        length = last_byte - first_byte + 1  # 此次读取的长度（字节）
        resp = StreamingHttpResponse(file_iterator(file_path, offset=first_byte, length=length), status=200, content_type=content_type)
        resp['Content-Length'] = str(length)
        resp['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, size)
    else:
        resp = StreamingHttpResponse(FileWrapper(open(file_path, 'rb')), content_type=content_type)
        resp['Content-Length'] = str(size)
    resp['Accept-Ranges'] = 'bytes'
    return resp
