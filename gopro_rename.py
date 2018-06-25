# -*- coding: utf-8 -*-
"""
Main file of the software Gopro File Organizer.

Gopro File Organizer is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Gopro File Organizer is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License v3.0 for more details.

You should have received a copy of the GNU Lesser General Public License v3.0
along with Gopro File Organizer. If not, see <http://www.gnu.org/licenses/> or
<https://opensource.org/licenses/LGPL-3.0>

Copyright (c) Alexander Stark 2018. 
"""



import os
import re

import shutil
import random
import datetime

# options to implement:
#   dryrun
#   force, overwrite exsiting files
#   verbose
#   copy (complete with all metadata)


def compile_filename(filename, directory=''):


    # check for single video or photo
    match = re.match('GOPR(\d{4})(\..*)', filename)

    if match:
        return os.path.join(directory, 'GoPro_%04d_%02d%s'.format(int(match.group(1)), 
                                                                  0, 
                                                                  match.group(2)))

    # check for chaptered video
    match = re.match('GP(\d{2})(\d{4})(\..*)', filename)
    if match:
        return os.path.join(directory, 'GoPro_%04d_%02d%s'.format(int(match.group(2)), 
                                                                  int(match.group(1)), 
                                                                  match.group(3)))

    # check for burst, time-lapse photo or looping video
    match = re.match('G(\d{3})(\d{4})(\..*)', filename)
    if match:
        return os.path.join(directory, 'GoPro_%04d_%02d%s'.format(int(match.group(2)), 
                                                                  int(match.group(1)), 
                                                                  match.group(3)))

    # check finally for 3D recording
    match = re.match('3D_(R|L)(\d{4})(\..*)', filename)
    if match:
        return os.path.join(directory, 'GoPro_%04d_%02d%s'.format(int(match.group(2)), 
                                                                  int(match.group(1)), 
                                                                  match.group(3)))

    print('Nothing matched. Nothing done.')

    return


"""
GoPro Naming convention:
Taken from the official website:
https://gopro.com/help/articles/question_answer/GoPro-Camera-File-Naming-Convention


Single Video    GOPRxxxx.mp4
Single Photo    GOPRxxxx.jpg



1. Get all files from a folder
2. Check at first for chaptered video and get also the first video, pop
    the found elements from list
2. check the list for single photo/ single video and pop those 
    elements form list
3. 

"""



def generate_random_test_names():
    test_file_list()
    return


def gen_rnd_file_list(number_of_files=10):
    
    rnd_single_files = []
    
    
    for ii in range(number_of_files):
        
        # the number 10000 is not include in the list.
        rnd_4digit_num = random.randrange(start=0, stop=10000, step=1)
        
        if bool(random.randrange(0,2,1)):
            ext_name = 'MP4'
        else:
            ext_name = 'JPG'
        
        
        filename = 'GOPR{0:d}.{1}'.format(rnd_4digit_num, ext_name)
        
        rnd_single_files.append(filename)
    
    return rnd_single_files
    

def gen_rnd_chap_list(number_of_files=10):
    
    rnd_chap_list = []
    
    
    for ii in range(number_of_files):
        
        # the number 10000 is not include in the list.
        rnd_4digit_num = random.randrange(start=0, stop=10000, step=1)
        
        ext_name = 'MP4'

        filename = 'GOPR{0:4d}.{1}'.format(rnd_4digit_num, ext_name)
        rnd_chap_list.append(filename)

        max_chap = 10
        number_of_sub_chap = random.randrange(start=1, stop=max_chap+1, step=1)
        
        
        for jj in range(number_of_sub_chap):
            
        
            filename = 'GO{0:2d}{1:4d}.{2}'.format(jj, rnd_4digit_num, ext_name)
            rnd_chap_list.append(filename)
    
    return rnd_chap_list


def gen_rnd_burst_loop_list(number_of_files=10):
    
    rnd_burst_loop_list = []
    
    for ii in range(number_of_files):
        
        # the number 10000 is not include in the list.
        rnd_4digit_num = random.randrange(start=0, stop=10000, step=1)
        
        if bool(random.randrange(0,2,1)):
            ext_name = 'MP4'
        else:
            ext_name = 'JPG'
        
        max_chap = 10
        number_of_bursts = random.randrange(start=1, stop=max_chap+1, step=1)
        
        offset = random.randrange(start=0, stop=1000-max_chap, step=1)
        
        for jj in range(number_of_bursts):
            
        
            filename = 'G{0:3}{1:4d}.{2}'.format(offset+jj, rnd_4digit_num, ext_name)
        
            rnd_burst_loop_list.append(filename)
    
    return rnd_burst_loop_list


test_file_list = [
# single videos and photos:
'GOPR1213.MP4',
'GOPR1214.MP4',
'GOPR1215.JPG',
'GOPR1216.MP4',
'GOPR1217.MP4',
'GOPR1218.JPG',
'GOPR1219.JPG',

# chaptered videos
'GOPR1212.MP4',
'GP011212.MP4',
'GP021212.MP4',

'GOPR1234.MP4',
'GP011234.MP4',
'GP021234.MP4',
'GP031234.MP4',
'GP041234.MP4',
'GP051234.MP4',

'GOPR1238.MP4',
'GP011238.MP4',
'GP021238.MP4',
'GP031238.MP4',
'GP041238.MP4',

# Burst, Time-Lapse Photos, Looping Videos:

'G0231111.JPG',
'G0231112.JPG',
'G0231113.JPG',
'G0231114.JPG',
'G0231115.JPG',
'G0231116.JPG',

'G0241117.JPG',
'G0241118.JPG',
'G0241119.JPG',
'G0241120.JPG',

'G0251121.JPG',
'G0251122.JPG',
'G0251123.JPG',
'G0251124.JPG',

# 3D record:

'3D_L0002.MP4',
'3D_R0002.MP4',

'3D_L0003.MP4',
'3D_R0003.MP4',

'3D_L0004.MP4',
'3D_R0004.MP4',

'3D_L0005.MP4',
'3D_R0005.MP4',

'3D_L1234.JPG',
'3D_R1234.JPG',

'3D_L1235.JPG',
'3D_R1235.JPG',

# should be left out:
'left out 1',
'1234',
'GOPRO1234.JPG',
'GO123.MP4',

]



def create_sorted_lists(filelist):
    """
    This logic applies to Camera Models: 
        HD HERO2, HERO3, HERO3+, HERO (2014), HERO Session, HERO4, 
        HERO5 Black, HERO5 Session.
        
    1. The Chaptered Video becomes

        GP<xx><zzzz>.MP4  ===> <YYYY>-<MM>-<DD>_<hh>H-<mm>m-<ss>s_<xx>_<zzzz>.MP4


    2. Burst, time-lapsed pictures or looping videos become

        G<yyy><zzzz>.<ext>  ===> <YYYY>-<MM>-<DD>_<hh>H-<mm>m-<ss>s_<yyy>_<zzzz>.MP4

    Note that the first part of such series will be translated as

        GP<xx><zzzz>.<ext> ===> <YYYY>-<MM>-<DD>_<hh>H-<mm>m-<ss>s_000_<zzzz>.MP4

    explicitly with file

    The following filename descripton are used:


        <ext>       placeholder for fileextentiom MP4, mp4, JPG or jpg 
        <xx>        placeholder for xx chapternumber
        <yyy>       placeholder for yyy burst number
        <zzzz>      placeholder for zzzz file number
        <YYYY>      year placeholder
        <MM>        month placeholder
        <DD>        day placeholder
        <hh>        hour placeholder in 24h notation
        <mm>        minutes placeholder
        <ss>        second placeholder  
        




    <YYYY>-<MM>-<DD>_<hh>H-<mm>m-<ss>s_<NN>.MP4
    <YYYY>-<MM>-<DD>_<hh>H-<mm>m-<ss>s_c<NN>.MP4
    """

    chap_vid_group_dict = {}
    single_element_list = []
    burst_time_lapsed_dict = {}
    record_3d_dict = {}

    # check at first chaptered videos:
    # ================================

    # need to reverse the iteration prozess to remove entries while stepping
    for entry in reversed(filelist):
        # check for chaptered video
        match = re.match('GP(\d{2})(\d{4})(\..*)', entry)
        if match:

            file_number = match.group(2)
            if chap_vid_group_dict.get(file_number) is None:
                chap_vid_group_dict[file_number] = [entry]
            else:
                # since the element 'entry' is iterated
                # reversely, it has to be appened at first place
                chap_vid_group_dict[file_number].insert(0, entry)

            filelist.remove(entry)

    # include also the first video to the dict
    for file_number in chap_vid_group_dict:

        first_video = 'GOPR{0}.MP4'.format(file_number)

        if first_video in filelist:
            filelist.remove(first_video)
            chap_vid_group_dict[file_number].insert(0, first_video)

    # extract now the burst/time-lapse/looping items:
    # ===============================================

    # need to reverse the iteration prozess to remove entries while stepping
    for entry in reversed(filelist):

        match = re.match('G(\d{3})(\d{4})(\..*)', entry)
        if match:
            
            group_number = match.group(1)
            
            if burst_time_lapsed_dict.get(group_number) is None:
                burst_time_lapsed_dict[group_number] = [entry]
            else:
                # since the element 'entry' is iterated
                # reversely, it has to be appened at first place
                burst_time_lapsed_dict[group_number].insert(0, entry)
                
            filelist.remove(entry)


    # extract now the 3D recordings:
    # ==============================

    for entry in reversed(filelist):
        match = re.match('3D_(R|L)(\d{4})(\..*)', entry)
        if match:
            
            file_number = match.group(2)
            
            if record_3d_dict.get(file_number) is None:
                record_3d_dict[file_number] = [entry]
            else:
                # just keep an order how L and R are attached to list
                if match.group(1) == 'L':
                    record_3d_dict[file_number].insert(0, entry)
                else:
                    record_3d_dict[file_number].append(entry)
        
            filelist.remove(entry)



    # finally, extract the single video/photos:
    #==========================================

    for entry in reversed(filelist):
        match = re.match('GOPR(\d{4})(\..*)', entry)
        if match:
            single_element_list.insert(0, entry)
            
            filelist.remove(entry)

    
    # return also the list of the remaining, unextracted files


    return chap_vid_group_dict, burst_time_lapsed_dict, record_3d_dict, single_element_list, filelist





def get_creation_date(filepath):
    timestamp = os.path.getctime(filepath)
    return datetime.datetime.fromtimestamp(timestamp)


def format_timestamp(filepath):
    datetime_obj = get_creation_date(filepath)
    return datetime_obj.strftime('%Y-%m-%d_%Hh%Mm%Ss')

def copy_with_meta(old_filename, new_filename):
    return shutil.copy2(old_filename, new_filename) 


def extract_from_files(test_file_list):
    chap, burst, record_3d, single, remaining_list = create_sorted_lists(test_file_list)

    print('Chaptered video:')
    print(chap,'\n')
    print('burst/time-lapse/looping items')
    print(burst,'\n')
    print('3D items')
    print(record_3d,'\n')
    print('Single Elements:')
    print(single,'\n')
    print('remaining list:')
    print(remaining_list)


if __name__ == '__main__':

#    extract_from_files(test_file_list)
    
#    print(gen_rnd_file_list())
#    print(gen_rnd_chap_list(number_of_files=10))
    print(gen_rnd_burst_loop_list())
    
    