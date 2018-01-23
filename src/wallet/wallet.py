import requests
import time
import base64
import ecdsa

node_url = 'http://localhost:5000/txion'

def welcome_msg():
    print("Welcome to Ushacoin")

def wallet():
    response = False

    while response not in ["1", "2", "3"]:
        response = input("""What do you want to do?
        1. Generate new wallet
        2. Send coins to another wallet
        3. Check transactions\n""")

    if response in "1":
        # Generate new wallet
        print("Make sure to save your credentials, or you will lose your wallet!")
        generate_ECDSA_keys()  

    elif response in "2":
        addr_from = input("From: introduce your wallet address (public key)\n")
        private_key = input("Introduce your private key\n")
        addr_to = input("To: introduce destination wallet address\n")
        amount = input("Amount: number stating how much do you want to send\n")

        print("=========================================\n\n")
        print("Is everything correct?\n")
        print("From: {0}\nPrivate Key: {1}\nTo: {2}\nAmount: {3}\n".format(addr_from, private_key, addr_to,amount))

        response = input("y/n\n")

        if response.lower() == "y":
            send_transaction(addr_from, private_key, addr_to, amount)

    elif response == "3":
        check_transactions()

def send_transaction(addr_from,private_key,addr_to,amount):
    # Debugging 
    #private_key="181f2448fa4636315032e15bb9cbc3053e10ed062ab0b2680a37cd8cb51f53f2"
    #amount="3000"
    #addr_from="SD5IZAuFixM3PTmkm5ShvLm1tbDNOmVlG7tg6F5r7VHxPNWkNKbzZfa+JdKmfBAIhWs9UKnQLOOL1U+R3WxcsQ=="
    #addr_to="SD5IZAuFixM3PTmkm5ShvLm1tbDNOmVlG7tg6F5r7VHxPNWkNKbzZfa+JdKmfBAIhWs9UKnQLOOL1U+R3WxcsQ=="
    
    if len(private_key) == 64:
        signature,message = sign_ECDSA_msg(private_key)
        payload = {"from": addr_from, "to": addr_to, "amount": amount, "signature": signature.decode(), "message": message}
        headers = {"Content-Type": "application/json"}

        res = requests.post(node_url, json = payload, headers = headers)
        print(res.text)

    else:
        print("Wrong address or key length! Verify and try again.")

def check_transactions():
    res = requests.get('http://localhost:5000/blocks')
    print(res.text)

def generate_ECDSA_keys():
    sk = ecdsa.SigningKey.generate(curve = ecdsa.SECP256k1) # Private key
    private_key = sk.to_string().hex() # Private key as hex

    vk = sk.get_verifying_key() # Public key
    public_key = vk.to_string().hex() # Public key as hex
    public_key = base64.b64encode(bytes.fromhex(public_key)) # Decode private key in order to make it shorter

    print("Private key: {0}".format(private_key))
    print("Wallet address / Public key: {0}".format(public_key.decode()))

def sign_ECDSA_msg(private_key):
    message = str(round(time.time()))
    bmessage = message.encode()
    sk = ecdsa.SigningKey.from_string(bytes.fromhex(private_key), curve = ecdsa.SECP256k1)
    signature = base64.b64encode(sk.sign(bmessage))

    return signature, message

if __name__ == '__main__':
    welcome_msg()
    wallet()
    input("Press any key to exit...")