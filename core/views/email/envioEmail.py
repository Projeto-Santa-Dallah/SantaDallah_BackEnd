from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

class EnviarEmailAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [] # Permite acesso a todos
    queryset = []  
    
    def post(self, request):
        user_email = request.data.get('user_email')  # E-mail do remetente
        assunto = 'Contato Santa Dallah'           # Assunto do e-mail
        mensagem = request.data.get('mensagem')            # Corpo da mensagem
        receptor = 'juliaifc22@gmail.com'                # E-mail do suporte/empresa

        # Verifica se os campos foram preenchidos
        if not user_email or not mensagem:
            return Response(
                {"error": "Todos os campos são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Cria o e-mail com o campo Reply-To
        email = EmailMessage(
            subject=assunto,
            body=mensagem,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[receptor],
            reply_to=[user_email],  # Configura o e-mail do cliente como "Reply-To"
        )

        # Tenta enviar o e-mail
        try:
            email.send(fail_silently=False)
            return Response({"success": "E-mail enviado com sucesso!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Erro ao enviar e-mail: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)