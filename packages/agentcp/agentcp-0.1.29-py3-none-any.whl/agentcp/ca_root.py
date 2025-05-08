import os

from agentcp.log import log_error, log_info
class CARoot:
    _instance = None
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.__initialized = False
        return cls._instance
    
    def set_ca_root_crt(self,ca_root_path):
        self.__ca_root_path = ca_root_path
    
    def __init__(self):
        self.__ca_crt = []
        # 内置根证书（PEM格式）
        self.__ca_crt.append("""\
-----BEGIN CERTIFICATE-----
MIICJzCCAYmgAwIBAgIRANRXvkNilsWkgDAZ2WopWj0wCgYIKoZIzj0EAwQwJzET
MBEGA1UEChMKQWdlbnRVbmlvbjEQMA4GA1UEAxMHUm9vdCBDQTAeFw0yNTA1MDYx
NDUzNDNaFw00NTA1MDYxNDUzNDNaMCcxEzARBgNVBAoTCkFnZW50VW5pb24xEDAO
BgNVBAMTB1Jvb3QgQ0EwgZswEAYHKoZIzj0CAQYFK4EEACMDgYYABABqZF2HVSqu
dR/yL0qtnvJM6Q6gBhv4RRWjW1QoOXIEtLg5LJbSBTvhNk0bhVeXLD5qeVNyGq/E
vjpEh/aesHpW+gGFRq3cxSvYfd5awJBUp5dcdOacdPTIbU+SzZ1jqDUHesXvJfh4
uQr23dUZr5S8k1iOsyew7H5xJSXQzSD93J9KJ6NTMFEwDgYDVR0PAQH/BAQDAgH+
MA8GA1UdJQQIMAYGBFUdJQAwDwYDVR0TAQH/BAUwAwEB/zAdBgNVHQ4EFgQUTNB4
Z8j+pPJcMoD5g27VvAufix4wCgYIKoZIzj0EAwQDgYsAMIGHAkFnQGYfL2M8nStV
YxHwdu1tInyC3SExSETFgKRoc/S0DuZM6iU2liTKitU6UF1hTlJ3atQ1BsfN5TM6
DJ/xWn9EEAJCAZOyKxqSjzWCn+0S4pdVxT0HxWrsraTwULBL312u+DF0q1fClCjE
0OStanrd6amm6PHsQhV3uJTOVH+ZR+bIGsJF
-----END CERTIFICATE-----
""")
        self.__ca_root_path = None
        self.__initialized = True
        
    def get_ca_root_crt_number(self):
        return len(self.__ca_crt)
    
    def get_ca_root_crt(self,index=0):
        if self.__ca_root_path:
            try:
                crt_files = sorted([f for f in os.listdir(self.__ca_root_path) if f.endswith('.crt')])
                if not crt_files:
                    log_error(f"目录 {self.__ca_root_path} 中没有证书文件")
                    return self.__ca_crt[index]
                    
                if index >= len(crt_files):
                    log_error(f"索引 {index} 超出文件数量 {len(crt_files)}")
                    return None
                    
                cert_path = os.path.join(self.__ca_root_path, crt_files[index])
                with open(cert_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except FileNotFoundError:
                log_error(f"根证书目录 {self.__ca_root_path} 不存在")
            except Exception as e:
                log_error(f"根读取证书文件失败: {str(e)}")
        return self.__ca_crt[index]