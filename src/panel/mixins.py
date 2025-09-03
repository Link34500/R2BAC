from django.views.generic import ListView
from .models import Log


__all__ = (
    "TableListMixin",
)

class Column:
    def __init__(self,title:str,rows:list=[]):
        self.title = title.capitalize()
        self.rows = rows

    def __str__(self):
        return self.as_html()

    def as_html(self):
        return "".join([f"<tr>{"".join([f"<td>{x}</td>" for x in i])}</tr>" for i in self.rows])
    
    def add_row(self,value):
        self.rows.append(value)

class Table():
    def __init__(self,columns:list=[]):
        self.columns:list[Column] = columns

    def __str__(self):
        return self.as_html()

    def as_html(self):
        columns_title = "".join([f"<th>{i.title}</th>" for i in self.columns])

        return f"""
        <table>
            <tr>
                {columns_title}
            </tr>
            
            {"".join([i.as_html() for i in self.columns])}

        </table>"""

    def add_column(self,title:str,rows:list=[]):
        instance = Column(title,rows)
        self.columns.append(instance)
        return instance

class TableListMixin(ListView):

    columns = ["__all__"]
    table_object_name = "table_objects"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        table = Table()
        objects = context[self.context_object_name]
        

        if '__all__' in self.columns:
            for obj in objects:
                vars(obj)
                self.columns.append("")
                
        for column in self.columns:
            attr = getattr(self.model,column)
            if attr:
                table.add_column(title=attr.verbose_name,rows=list(objects.object_list) if not self.paginate_by is None else list(objects))

        context.update({self.table_object_name:table})

        return context

