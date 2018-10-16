"""
form.errors 表单错误消息的提取
将form表单提交的结果，转换成json格式输出,从而得到error_message
定义一个表单父类，然后定义一个get_error，
定义的其他表单继承此类，从而有此属性，从而获取表单的错误信息
"""
class FormMixin(object):
    def get_error(self):
        if hasattr(self,'errors'):
            errors = self.errors.get_json_data()
            error_tuple = errors.popitem()
            error_list = error_tuple[1]
            error_dict = error_list[0]
            message = error_dict['message']
            return message
        else:
            return None

