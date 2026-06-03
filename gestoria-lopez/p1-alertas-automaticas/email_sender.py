# email_sender.py
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

import os

load_dotenv()

logger = logging.getLogger(__name__)

EMAIL_REMITENTE = os.getenv("EMAIL_REMITENTE")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


# ── EXCEPCIONES ────────────────────────────────────────────
class EmailError(Exception):
    pass


# ── PLANTILLA HTML ─────────────────────────────────────────
# Genera el cuerpo del email en HTML para un cliente concreto
# con todas sus alertas agrupadas — un email por cliente,
# no un email por alerta.
def generar_html(cliente: str, alertas: list) -> str:
    filas = ""
    for alerta in alertas:
        if alerta.dias_restantes <= 5:
            color = "#D32F2F"
            bg = "#FFEBEE"
            urgencia = "🚨 Urgente"
        elif alerta.dias_restantes <= 15:
            color = "#E67E00"
            bg = "#FFF3E0"
            urgencia = "⚠️ Próxima"
        else:
            color = "#2E7D32"
            bg = "#E8F5E9"
            urgencia = "📅 En plazo"

        filas += f"""
        <tr>
            <td style="padding:10px 14px; border-bottom:1px solid #F0F3F8;">{alerta.obligacion}</td>
            <td style="padding:10px 14px; border-bottom:1px solid #F0F3F8;">{alerta.fecha_vencimiento.strftime('%d/%m/%Y')}</td>
            <td style="padding:10px 14px; border-bottom:1px solid #F0F3F8; text-align:center;">
                <span style="background:{bg}; color:{color}; padding:3px 10px; border-radius:20px; font-size:13px; font-weight:500;">
                    {alerta.dias_restantes} días
                </span>
            </td>
            <td style="padding:10px 14px; border-bottom:1px solid #F0F3F8; color:{color};">{urgencia}</td>
        </tr>
        """

    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head><meta charset="UTF-8"></head>
    <body style="margin:0; padding:0; background:#F4F6F9; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">

        <div style="max-width:600px; margin:32px auto; background:#FFFFFF; border-radius:12px; overflow:hidden; border:1px solid #E5E9F0;">

            <!-- Cabecera -->
            <div style="background:#3D2B1F; padding:24px 32px;">
                <p style="margin:0; color:#F5EDE8; font-size:18px; font-weight:600;">Gestoría López & Asociados</p>
                <p style="margin:4px 0 0; color:#A8836F; font-size:13px;">Sistema de Alertas Fiscales</p>
            </div>

            <!-- Cuerpo -->
            <div style="padding:32px;">
                <p style="font-size:15px; color:#1A2C4E; margin:0 0 8px;">Estimado/a <strong>{cliente}</strong>,</p>
                <p style="font-size:14px; color:#8A96A8; margin:0 0 24px; line-height:1.6;">
                    Le informamos de los próximos vencimientos fiscales que requieren su atención.
                    Por favor, revise las fechas indicadas y contacte con nosotros si necesita cualquier aclaración.
                </p>

                <!-- Tabla de alertas -->
                <table style="width:100%; border-collapse:collapse; font-size:14px;">
                    <thead>
                        <tr style="background:#F4F6F9;">
                            <th style="padding:10px 14px; text-align:left; color:#8A96A8; font-weight:500; font-size:12px; text-transform:uppercase; letter-spacing:0.05em;">Obligación</th>
                            <th style="padding:10px 14px; text-align:left; color:#8A96A8; font-weight:500; font-size:12px; text-transform:uppercase; letter-spacing:0.05em;">Fecha límite</th>
                            <th style="padding:10px 14px; text-align:center; color:#8A96A8; font-weight:500; font-size:12px; text-transform:uppercase; letter-spacing:0.05em;">Días restantes</th>
                            <th style="padding:10px 14px; text-align:left; color:#8A96A8; font-weight:500; font-size:12px; text-transform:uppercase; letter-spacing:0.05em;">Estado</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filas}
                    </tbody>
                </table>

                <p style="font-size:13px; color:#8A96A8; margin:24px 0 0; line-height:1.6;">
                    Este mensaje ha sido generado automáticamente por el sistema de alertas de Gestoría López & Asociados.<br>
                    Para cualquier consulta, responda a este correo o llámenos.
                </p>
            </div>

            <!-- Pie -->
            <div style="background:#F4F6F9; padding:16px 32px; border-top:1px solid #E5E9F0;">
                <p style="margin:0; font-size:12px; color:#8A96A8;">
                    Gestoría López & Asociados · Madrid, España
                </p>
            </div>

        </div>
    </body>
    </html>
    """


# ── ENVÍO ──────────────────────────────────────────────────
# Envía un email HTML a un destinatario con las alertas del cliente.
# Usa SMTP con TLS — el estándar de Gmail.
def enviar_email(destinatario: str, cliente: str, alertas: list) -> bool:
    if not EMAIL_REMITENTE or not EMAIL_PASSWORD:
        raise EmailError("Credenciales de email no configuradas en .env")

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"⚠️ Alertas fiscales — {cliente}"
        msg["From"] = f"Gestoría López & Asociados <{EMAIL_REMITENTE}>"
        msg["To"] = destinatario

        html = generar_html(cliente, alertas)
        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
            servidor.starttls()
            servidor.login(EMAIL_REMITENTE, EMAIL_PASSWORD)
            servidor.sendmail(EMAIL_REMITENTE, destinatario, msg.as_string())

        logger.info(f"Email enviado correctamente a {destinatario} — {cliente}")
        return True

    except smtplib.SMTPAuthenticationError:
        raise EmailError("Credenciales incorrectas — revisa el .env")
    except smtplib.SMTPException as e:
        raise EmailError(f"Error SMTP: {e}")
    except Exception as e:
        raise EmailError(f"Error inesperado: {e}")


# ── ENVÍO MASIVO ───────────────────────────────────────────
# Agrupa las alertas por cliente y envía un email a cada uno.
# Devuelve un resumen de cuántos emails se enviaron y cuántos fallaron.
def enviar_alertas_masivo(alertas: list, emails_clientes: dict) -> dict:
    # Agrupamos alertas por cliente
    por_cliente = {}
    for alerta in alertas:
        if alerta.cliente not in por_cliente:
            por_cliente[alerta.cliente] = []
        por_cliente[alerta.cliente].append(alerta)

    enviados = 0
    fallidos = 0

    for cliente, alertas_cliente in por_cliente.items():
        destinatario = emails_clientes.get(cliente)
        if not destinatario:
            logger.warning(f"Cliente sin email configurado: {cliente}")
            fallidos += 1
            continue

        try:
            enviar_email(destinatario, cliente, alertas_cliente)
            enviados += 1
        except EmailError as e:
            logger.error(f"Error enviando email a {cliente}: {e}")
            fallidos += 1

    return {"enviados": enviados, "fallidos": fallidos}
