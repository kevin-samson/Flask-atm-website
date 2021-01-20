from itsdangerous import TimedJSONWebSignatureSerializer as ser
from itsdangerous.exc import BadSignature

def verfyToken(token):
    s = ser('5791628bb0b13ce0c676dfde280ba245')
    try:
        data = s.loads(token)
    except:
        return None
    if data:
        if 'email' in data:
            the_email = s.loads(token)['user_id']
            return the_email
        elif 'mode' in data:
            return s.loads(token)['amount'], s.loads(token)['mode']

print(verfyToken('eyJhbGciOiJIUzUxMiIsImlhdCI6MTYxMTE2Nzc3MywiZXhwIjoxNjExMTY5NTczfQ.eyJtb2RlIjoiZHJhdyIsImFtb3VudCI6NTB9.wIfWD0vP83jO-mnARmg5ZwX7AAdMPwDxvmbQ4nrpMjPHimi_sfRRjeyFeSr5c5HnmjFfqeN06nAAK2HolvKltw'))