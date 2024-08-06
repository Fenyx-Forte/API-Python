import base64
import os

from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Attachment,
    ContentId,
    Disposition,
    FileContent,
    FileName,
    FileType,
    Mail,
)


def transform_image_in_base64(image_path: str) -> str:
    image_bytes = open(image_path, "rb").read()

    image_bytes_encode = base64.b64encode(image_bytes)

    image_string = image_bytes_encode.decode()

    return image_string


def embedded_image(image_path: str) -> str:
    image_string = transform_image_in_base64(image_path)

    return f"data:image/png;base64,{image_string}"


def enviar_email_teste() -> None:
    conteudo_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title> Relatório ENADE </title>
    </head>
    <body>
        <table role="presentation" style="width: 100%; height: 100%;">
            <tr>
                <td align="center">
                    <table role="presentation" style="width: 600px; max-width: 100%">
                        <tr>
                            <td style="text-align: left;">
                                <img src="cid:capa" alt="Capa" style="display: block; margin: 0 auto; max-width: 50%; height: auto;">
                                <br/>
                                <br/>
                                <h1> Relatório ENADE </h1>
                                <p>
                                    Prezados gestores,
                                    <br/>
                                    <br/>
                                    Segue análise do resultado do ENADE 2021.
                                    <br/>
                                    <br/>
                                    <br/>
                                    Atencionsamente,
                                    <br/>
                                    Fenyx Forte.
                                    <br/> <a href="https://fenyx-forte.github.io/">Veja meu portfólio</a>.
                                </p>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """

    caminho_pdf = "relatorios/enade_2021.pdf"

    caminho_logo_enade = "recursos/images/logo_enade.png"

    with open(caminho_pdf, "rb") as f:
        conteudo_pdf = f.read()

    encoded_pdf = base64.b64encode(conteudo_pdf).decode()

    encoded_capa = transform_image_in_base64(caminho_logo_enade)

    anexo = Attachment()
    anexo.file_content = FileContent(encoded_pdf)
    anexo.file_type = FileType("application/pdf")
    anexo.file_name = FileName("enade_2021.pdf")
    anexo.disposition = Disposition("attachment")
    anexo.content_id = ContentId("Example Content ID")

    anexo_capa = Attachment()
    anexo_capa.file_content = FileContent(encoded_capa)
    anexo_capa.file_type = FileType("image/png")
    anexo_capa.file_name = FileName("imagem.png")
    anexo_capa.disposition = Disposition("inline")
    anexo_capa.content_id = ContentId("capa")

    load_dotenv()

    message = Mail(
        from_email=os.getenv("SENDER_EMAIL"),
        to_emails=os.getenv("RECIPIENT_EMAIL"),
        subject="Enviando email com o Sendgrid",
        html_content=conteudo_html,
    )

    message.add_attachment(anexo)
    message.add_attachment(anexo_capa)

    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
