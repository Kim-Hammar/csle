from csle_common.metastore.metastore_facade import MetastoreFacade

if __name__ == '__main__':
    execution = MetastoreFacade.get_emulation_execution(ip_first_octet=15, emulation_name="csle-level14-090")
    print(execution.emulation_env_config.elk_config.container.ips_and_networks)
