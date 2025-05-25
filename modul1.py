import argparse
import asyncio
from pysnmp.hlapi.asyncio import *
import networkx as nx
import matplotlib.pyplot as plt

# SNMP'den veri alma fonksiyonu
async def get_snmp_data(ip_address, community, oid):
    #transport = await UdpTransportTarget.create((ip_address, 161))
    transport = UdpTransportTarget((ip_address, 161))
    #errorIndication, errorStatus, errorIndex, varBinds = await get_cmd(
    errorIndication, errorStatus, errorIndex, varBinds = await getCmd(

        SnmpEngine(),
        CommunityData(community),
        transport,
        ContextData(),
        ObjectType(ObjectIdentity(oid))
    )

    if errorIndication:
        print(f"[{ip_address}] Hata: {errorIndication}")
        return None
    elif errorStatus:
        print(f"[{ip_address}] Hata Durumu: {errorStatus.prettyPrint()} (Index: {errorIndex})")
        return None
    else:
        for varBind in varBinds:
            return varBind[1].prettyPrint()

# CLI üzerinden parametreleri alma
def parse_args():
    parser = argparse.ArgumentParser(description="SNMP tabanlı Ağ Topolojisi Görselleştirme Aracı")
    parser.add_argument("--ips", nargs="+", required=True, help="IP adreslerini boşlukla ayırarak girin (örn: 192.168.1.1 192.168.1.2)")
    parser.add_argument("--community", default="public", help="Community string (varsayılan: public)")
    return parser.parse_args()

# Ağ grafiği oluşturma
def create_network_graph(devices, links):
    G = nx.Graph()
    for device, info in devices.items():
        G.add_node(device, **info)
    for source, target, attributes in links:
        G.add_edge(source, target, **attributes)
    return G

# Grafiği çiz
def draw_network_graph(graph):
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_size=1500, node_color="skyblue",
            font_size=10, font_weight="bold", edge_color="gray", linewidths=0.5, alpha=0.8)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=nx.get_edge_attributes(graph, 'type'))
    plt.title("Ağ Topolojisi")
    plt.show()

# Grafiği PNG olarak kaydet
def save_graph_to_png(graph, filename="network_topology_format1.png"):
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_size=1500, node_color="skyblue",
            font_size=10, font_weight="bold", edge_color="gray", linewidths=0.5, alpha=0.8)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=nx.get_edge_attributes(graph, 'type'))
    plt.title("Ağ Topolojisi")
    plt.savefig(filename)
    print(f"[+] Grafik '{filename}' olarak kaydedildi.")

# Ana program
async def main():
    args = parse_args()
    ip_list = args.ips
    community_string = args.community

    devices = {}
    links = []

    # SNMP ile cihazlardan isim bilgisi çek
    for idx, ip in enumerate(ip_list):
        sys_name = await get_snmp_data(ip, community_string, "1.3.6.1.2.1.1.5.0")
        if sys_name:
            device_name = f"{sys_name} ({ip})"
        else:
            device_name = f"Cihaz-{idx+1} ({ip})"

        devices[device_name] = {"type": "unknown", "ip": ip}

        # Basit bağlantı modelleme (sırayla birbirine bağla)
        if idx > 0:
            prev_device = list(devices.keys())[idx - 1]
            links.append((prev_device, device_name, {"type": "ethernet", "speed": "1Gbps"}))

    graph = create_network_graph(devices, links)
    draw_network_graph(graph)
    save_graph_to_png(graph)

# Çalıştır
if __name__ == "__main__":
    asyncio.run(main())












































#çalışmadı ilk kod
"""
from pysnmp.hlapi.asyncio import *

def get_snmp_data(ip_address, community, oid):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(community),
               UdpTransportTarget((ip_address, 161)),
               ContextData(),
               ObjectType(ObjectIdentity(oid)))
    )

    if errorIndication:
        print(f"Hata: {errorIndication}")
        return None
    elif errorStatus:
        print(f"Hata Durumu: {errorStatus.prettyPrint()}")
        print(f"Hata İndeksi: {errorIndex}")
        return None
    else:
        for varBind in varBinds:
            return varBind[1].prettyPrint()

# Örnek kullanım
router_ip = "192.168.1.1"
community_string = "public"

system_name = get_snmp_data(router_ip, community_string, "1.3.6.1.2.1.1.5.0")
if system_name:
    print(f"{router_ip} cihazının adı: {system_name}")
import networkx as nx

def create_network_graph(devices, links):
    G = nx.Graph()
    for device, info in devices.items():
        G.add_node(device, **info)
    for source, target, attributes in links:
        G.add_edge(source, target, **attributes)
    return G

# Örnek cihaz ve bağlantı verileri (SNMP'den toplanan verilere göre düzenlenmeli)
devices = {
    "Router1": {"type": "router", "model": "XYZ"},
    "Switch1": {"type": "switch", "model": "ABC"},
    "Server1": {"type": "server", "os": "Linux"}
}

links = [
    ("Router1", "Switch1", {"type": "ethernet", "speed": "1Gbps"}),
    ("Switch1", "Server1", {"type": "ethernet", "speed": "1Gbps"})
]

graph = create_network_graph(devices, links)

import matplotlib.pyplot as plt

def draw_network_graph(graph):
    pos = nx.spring_layout(graph)  # Farklı layout algoritmaları deneyebilirsiniz (circular_layout, kamada_kawai_layout vb.)
    nx.draw(graph, pos, with_labels=True, node_size=1500, node_color="skyblue", font_size=10, font_weight="bold", edge_color="gray", linewidths=0.5, alpha=0.8)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=nx.get_edge_attributes(graph, 'type'))
    plt.title("Ağ Topolojisi")
    plt.show()

# Oluşturulan grafiği çizdirme
draw_network_graph(graph)

def save_graph_to_png(graph, filename="network_topology.png"):
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_size=1500, node_color="skyblue", font_size=10, font_weight="bold", edge_color="gray", linewidths=0.5, alpha=0.8)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=nx.get_edge_attributes(graph, 'type'))
    plt.title("Ağ Topolojisi")
    plt.savefig(filename)
    print(f"Grafik '{filename}' olarak kaydedildi.")

# Grafiği PNG olarak kaydetme
save_graph_to_png(graph)

"""


