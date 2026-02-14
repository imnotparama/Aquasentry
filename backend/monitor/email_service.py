from django.core.mail import send_mail
from django.conf import settings
import threading

def send_alert_email(report_instance):
    """
    Sends an email alert for high-severity health reports.
    Runs in a separate thread to avoid blocking the API response.
    """
    # For testing: Send email for ALL severity levels (usually < 7 returns)
    if report_instance.severity < 1: 
        print(f"ℹ️ Severity {report_instance.severity} is too low for alert.")
        return

    subject = f"🚨 URGENT: High Severity Health Alert - {report_instance.get_symptom_type_display()}"
    
    message = f"""
    CRITICAL HEALTH ALERT
    --------------------------------------------------
    A high-severity health issue has been reported in the monitoring system.

    Category: {report_instance.get_symptom_type_display()}
    Severity: {report_instance.severity}/10
    Location: Lat {report_instance.latitude}, Lon {report_instance.longitude}
    Timestamp: {report_instance.submitted_at}
    
    Notes:
    {report_instance.notes}

    --------------------------------------------------
    Please investigate immediately. 
    Sent via AquaSentry System.
    """
    
    recipient_list = [settings.EMAIL_HOST_USER] # Send to self/admin for demo purposes

    def _send():
        try:
            if settings.EMAIL_HOST_USER == 'YOUR_EMAIL_ADDRESS@gmail.com':
                print("⚠️  Email not sent: EMAIL_HOST_USER not set in settings.py")
                print(f"--- [SIMULATION] Email Content ---\n{message}\n----------------------------------")
                return

            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
            print(f"✅ Alert email sent to {recipient_list}")
        except Exception as e:
            print(f"❌ Failed to send email: {e}")

    # Run asynchronously
    email_thread = threading.Thread(target=_send)
    email_thread.start()
