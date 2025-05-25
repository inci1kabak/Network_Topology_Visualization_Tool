# Network_Topology_Visualization_Tool

#### Kullanılan Araçlar ve Kütüphaneler
Araç/Kütüphane	                              Açıklama
Python 3.x	                              Ana programlama dili.
argparse	                                Komut satırı argümanlarını almak için (standart kütüphane).
asyncio	                                  Asenkron programlama için (standart kütüphane).
pysnmp	                                  SNMP üzerinden cihaz bilgisi almak için. pysnmp kütüphanesinin hlapi.asyncio modülü kullanılmış.
networkx	                                Ağ grafikleri (topoloji) oluşturmak için.
matplotlib.pyplot	                        Ağ topolojisinin görsel olarak çizilmesi için.
random	                                  Rastgele bağlantıların oluşturulması için (standart kütüphane)

#### Kurulum Ortamı Gereksinimleri:
pip install pysnmp networkx matplotlib

#### Çalışma Ortamı
VS Code (Visual Studio Code): Kodu yazmak ve çalıştırmak için kullanılan geliştirme ortamı.

Komut satırı (Terminal / PowerShell): Python dosyasını çalıştırmak ve git işlemleri için kullanılan ortam.

Git & GitHub: Kodunuzu bir sürüm kontrol sistemiyle yönetmek ve GitHub’a yüklemek için.


#### Gerçek Ortamda SNMP Kullanımı İçin Gerekenler
SNMP'den gerçek veri almak için, aşağıdakilere ihtiyaç vardır:

SNMP aktif cihazlar (örneğin router, switch, server vb.).

Cihazlarda SNMP servisi açık olmalı (genellikle port 161).

SNMP community string (örneğin: public, private).

Network'te bu cihazlara erişim (aynı ağda olmak ya da yönlendirme yapılmış olması).
