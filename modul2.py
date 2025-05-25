import argparse
import asyncio
from pysnmp.hlapi.asyncio import *
import networkx as nx
import matplotlib.pyplot as plt
import random

async def get_snmp_data(ip_address, community, oid):
    transport = UdpTransportTarget((ip_address, 161))
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

def parse_args():
    parser = argparse.ArgumentParser(description="SNMP tabanlı Ağ Topolojisi Görselleştirme Aracı")
    parser.add_argument("--ips", nargs="+", required=True, help="IP adreslerini boşlukla ayırarak girin")
    parser.add_argument("--community", default="public", help="Community string (varsayılan: public)")
    return parser.parse_args()

def detect_device_type(sys_descr):
    if not sys_descr:
        return "unknown"
    sys_descr = sys_descr.lower()
    if "router" in sys_descr:
        return "router"
    elif "switch" in sys_descr:
        return "switch"
    elif "server" in sys_descr or "linux" in sys_descr or "windows" in sys_descr:
        return "server"
    else:
        return "unknown"

def create_network_graph(devices, links):
    G = nx.Graph()
    for device, info in devices.items():
        G.add_node(device, **info)
    for source, target, attributes in links:
        G.add_edge(source, target, **attributes)
    return G

def draw_network_graph(graph):
    pos = nx.kamada_kawai_layout(graph)

    # Cihaz tipine göre renk haritası
    color_map = {
        "router": "red",
        "switch": "green",
        "server": "blue",
        "unknown": "gray"
    }

    # Cihaz tipine göre şekil haritası
    shape_map = {
        "router": "s",   # square
        "switch": "o",   # circle
        "server": "D",   # diamond
        "unknown": "^"   # triangle_up
    }

    # Her cihaz tipini ayrı çizelim
    for device_type in set(nx.get_node_attributes(graph, 'type').values()):
        nodelist = [n for n, attr in graph.nodes(data=True) if attr['type'] == device_type]
        nx.draw_networkx_nodes(
            graph, pos, nodelist=nodelist,
            node_color=color_map.get(device_type, "gray"),
            node_shape=shape_map.get(device_type, "o"),
            node_size=1800,
            alpha=0.9,
            label=device_type.capitalize()
        )

    nx.draw_networkx_labels(graph, pos, font_weight="bold")
    nx.draw_networkx_edges(graph, pos, edge_color="gray", width=1)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=nx.get_edge_attributes(graph, 'type'))
    plt.legend(title="Cihaz Tipleri")
    plt.title("Ağ Topolojisi")
    plt.show()

def save_graph_to_png(graph, filename="network_topology_format2.png"):
    pos = nx.kamada_kawai_layout(graph)

    color_map = {
        "router": "red",
        "switch": "green",
        "server": "blue",
        "unknown": "gray"
    }

    shape_map = {
        "router": "s",
        "switch": "o",
        "server": "D",
        "unknown": "^"
    }

    for device_type in set(nx.get_node_attributes(graph, 'type').values()):
        nodelist = [n for n, attr in graph.nodes(data=True) if attr['type'] == device_type]
        nx.draw_networkx_nodes(
            graph, pos, nodelist=nodelist,
            node_color=color_map.get(device_type, "gray"),
            node_shape=shape_map.get(device_type, "o"),
            node_size=1800,
            alpha=0.9,
            label=device_type.capitalize()
        )

    nx.draw_networkx_labels(graph, pos, font_weight="bold")
    nx.draw_networkx_edges(graph, pos, edge_color="gray", width=1)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=nx.get_edge_attributes(graph, 'type'))
    plt.legend(title="Cihaz Tipleri")
    plt.title("Ağ Topolojisi")
    plt.savefig(filename)
    print(f"[+] Grafik '{filename}' olarak kaydedildi.")

async def main():
    args = parse_args()
    ip_list = args.ips
    community_string = args.community

    devices = {}

    # Önce cihaz bilgilerini alalım
    for idx, ip in enumerate(ip_list):
        sys_name = await get_snmp_data(ip, community_string, "1.3.6.1.2.1.1.5.0")  # sysName
        sys_descr = await get_snmp_data(ip, community_string, "1.3.6.1.2.1.1.1.0")  # sysDescr
        device_type = detect_device_type(sys_descr)

        if sys_name:
            device_name = f"{sys_name} ({ip})"
        else:
            device_name = f"Cihaz-{idx+1} ({ip})"

        devices[device_name] = {"type": device_type, "ip": ip}

    # Rastgele bağlantılar oluşturalım (her cihaz 1-3 arası bağlantıya sahip olabilir)
    links = []
    device_names = list(devices.keys())
    for device in device_names:
        max_links = min(3, len(device_names)-1)
        link_count = random.randint(1, max_links)  # her cihaz 1 ile max_links arasında bağlantı kuracak
        targets = random.sample([d for d in device_names if d != device], link_count)
        for target in targets:
            # Aynı bağlantıyı tekrar eklememek için kontrol
            if (device, target) not in links and (target, device) not in links:
                links.append((device, target, {"type": "ethernet", "speed": "1Gbps"}))

    graph = create_network_graph(devices, links)
    draw_network_graph(graph)
    save_graph_to_png(graph)

if __name__ == "__main__":
    asyncio.run(main())



