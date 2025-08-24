from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from common.divers.context_processors import contexts

class Mail:
    class Sender:
        def __init__(self,mail):
            self.mail = mail

        def send_mail(self,request,objet,destinataires:list,template='',context:dict={},text=''):
            context.update({"request":request})
            context.update(contexts())
        
            html = render_to_string(f"{template}",context=context)
            email = EmailMultiAlternatives(
                objet,
                text,
                self.mail,
                destinataires,
                headers={"Reply-To":"contact@r2bac.fr"}
            )
            email.attach_alternative(html,"text/html")
            email.send()

    support = Sender("support@r2bac.fr")
    noreply = Sender("no-reply@r2bac.fr")