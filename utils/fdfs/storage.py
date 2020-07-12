from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client, get_tracker_conf
from django.conf import settings


# 文件存储类
class FDFSStorage(Storage):
    """fast dfs文件存储类"""

    def __init__(self, client_conf=None, base_url=None):
        if base_url is None:
            base_url = settings.FDFS_URL
        self.base_url = base_url

    def _open(self, name, mode='rb'):
        """打开文件时使用"""
        pass

    def _save(self, name, content):
        """保存文件时使用"""
        # name:你选择上传文件的名字
        # content:包含你上传文件内容的File对象

        # 创建一个Fdfs_client对象
        trackers = get_tracker_conf('/Users/chenqiangjun/go/dailyfresh/utils/fdfs/client.conf')
        client = Fdfs_client(trackers)

        # 上传文件到fast dfs文件系统中
        res = client.upload_by_buffer(content.read())

        # res = 返回的字典
        # dict
        # {
        #     'Group name': group_name,
        #     'Remote file_id': remote_file_id,
        #     'Status': 'Upload successed.',
        #     'Local file name': '',
        #     'Uploaded size': upload_size,
        #     'Storage IP': storage_ip
        # }
        if res.get('Status') != 'Upload successed.':
            # 上传失败
            raise Exception('上传文件到fast DFS失败')

        # 获取返回的文件ID
        filename = res.get('Remote file_id')

        return filename.decode()

    def exists(self, name):
        # 因为 文件是存储在 fastdfs文件系统中的，所以 对于django来说：不存在 文件名不可用 的情况
        return False

    def url(self, name):
        """返回访问文件的url路径"""
        return self.base_url + name
