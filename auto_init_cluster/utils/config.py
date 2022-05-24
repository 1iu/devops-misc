#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import toml
import os
import logging


class ClusterServer:

    def __init__(self, config_dict):
        self.username = ''
        self.password = ''
        self.hosts = []
        self.hostnames = []
        self.jdk_source = ''
        self.jdk_path = ''
        self.hadoop_source = ''
        self.hadoop_path = ''
        self.scala_source = ''
        self.scala_path = ''
        self.spark_source = ''
        self.spark_path = ''
        self.ntp_server = ''
        for k in config_dict:
            setattr(self, k, config_dict[k])


class SparkServer:

    def __init__(self, config_dict):
        self.master = ''
        self.port = ''
        self.spark_hosts = []
        self.spark_hostnames = []
        self.default_cores = -1
        for k in config_dict:
            setattr(self, k, config_dict[k])


class HadoopServer:

    def __init__(self, config_dict):
        self.master = ''
        self.port = ''
        self.hadoop_hosts = []
        self.hadoop_hostnames = []
        self.tmp_folder = ''
        self.data_folder = ''
        for k in config_dict:
            setattr(self, k, config_dict[k])


class ClusterConfig:

    def __init__(self, path):
        self.logger = logging.getLogger()
        if not os.path.exists(path):
            self.logger.error('no config in path: %s', path)
            raise FileNotFoundError
        self.config = toml.load(open(path, encoding='utf-8'))
        self.server = ClusterServer(self.config['server'])
        self.hadoop = HadoopServer(self.config['hadoop'])
        self.spark = SparkServer(self.config['spark'])


class PassPhrase:

    def __init__(self, path):
        self.logger = logging.getLogger()
        if not os.path.exists(path):
            self.logger.error('no passphrase in path: %s', path)
            raise FileNotFoundError
        config = toml.load(open(path, encoding='utf-8'))
        try:
            self.username = config['username']
            self.password = config['password']

        except KeyError as e:
            self.logger.error('Config key error: %s', e)
            raise e
