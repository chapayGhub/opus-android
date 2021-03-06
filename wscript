#! /usr/bin/env python
# encoding: utf-8

import os

APPNAME = 'opus-android'
VERSION = '0.0.0'


def configure(conf):

    conf.check_cxx(lib='android')

def build(bld):


    CXX = bld.env.get_flat("CXX")
    # Matches both g++ and clang++
    if 'g++' in CXX or 'clang' in CXX:
        # The -fPIC flag is required for all underlying static libraries that
        # will be included in any shared libraries built in this project
        bld.env.append_value('CXXFLAGS', '-fPIC')
        bld.env.append_value('CFLAGS', '-fPIC')

    bld.env.append_unique(
        'DEFINES_STEINWURF_VERSION',
        'STEINWURF_OPUS_ANDROID_VERSION="{}"'.format(VERSION))

    bld.recurse('jni')

    if bld.is_toplevel():

        # Install the APK files from the gradle build output folder:
        # app/gradle_build/outputs/apk/debug
        if bld.has_tool_option('install_path'):

            install_path = bld.get_tool_option('install_path')
            install_path = os.path.abspath(os.path.expanduser(install_path))
            relative_dir = bld.bldnode.path_from(bld.srcnode)

            app = 'app'
            start_dir = bld.path.find_dir(
                '{}/gradle_build/outputs/apk/debug'.format(app))
            bld.install_files(os.path.join(install_path, relative_dir),
                                start_dir.ant_glob('*.apk'),
                                cwd=start_dir)
