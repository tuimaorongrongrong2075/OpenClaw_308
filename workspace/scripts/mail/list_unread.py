import os
import imaplib
import email

imap_user = os.environ.get('QQMAIL_PERSONAL_USER', '')
auth = os.environ.get('QQMAIL_PERSONAL_AUTH_CODE', '')

mail = imaplib.IMAP4_SSL('imap.qq.com')
mail.login(imap_user, auth)
mail.select('INBOX')

# Get all unread
typ, all_msgs = mail.search(None, 'UNSEEN')
all_ids = all_msgs[0].split()

for msg_id in all_ids[:10]:
    typ, msg_data = mail.fetch(msg_id, '(RFC822)')
    msg = email.message_from_bytes(msg_data[0][1])
    
    # Decode subject
    subject_raw = msg['Subject']
    if subject_raw:
        decoded = email.header.decode_header(subject_raw)
        subject = decoded[0][0]
        if isinstance(subject, bytes):
            subject = subject.decode('utf-8', errors='ignore')
    
    # Decode from
    from_raw = msg['From']
    if from_raw:
        decoded_from = email.header.decode_header(from_raw)
        from_addr = decoded_from[0][0]
        if isinstance(from_addr, bytes):
            from_addr = from_addr.decode('utf-8', errors='ignore')
    
    print(f'📩 {subject}')
    print(f'   📧 {from_addr}')
    print()

mail.logout()
