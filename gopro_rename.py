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
import subprocess
import json

from PIL import Image

# options to implement:
#   dryrun
#   force, overwrite exsiting files
#   verbose
#   copy (complete with all metadata)

__version__ = 0.1
__author__ = 'Alexander Stark'


def compile_filename(filename, directory='.'):


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
    """ Return a manual test list for filename detection. 
    
    Returns
    -------
    list
        a test file list with string entries
    """
    return test_file_list


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

# =============================================================================
# Random file list generation to test the find and sort algorithm


def gen_rnd_file_list(number_of_files=10):
    """ Generate a random file list of single photos and videos
    
    Returns
    -------
    list
        a list with random valid GoPro string names for single photos and videos        
    """
    
    rnd_single_files = []
    
    
    for ii in range(number_of_files):
        
        # the number 10000 is not include in the list.
        rnd_4digit_num = random.randrange(start=0, stop=10000, step=1)
        
        if bool(random.randrange(0,2,1)):
            ext_name = 'MP4'
        else:
            ext_name = 'JPG'
        
        
        filename = 'GOPR{0:04d}.{1}'.format(rnd_4digit_num, ext_name)
        
        rnd_single_files.append(filename)
    
    return rnd_single_files
    

def gen_rnd_chap_list(number_of_files=10):
    """ Generate a random chaptered list of only videos
    
    Returns
    -------
    list
        a list with random and valid GoPro string names for chaptered videos. 
    """
    
    rnd_chap_list = []
    
    
    for ii in range(number_of_files):
        
        # the number 10000 is not include in the list.
        rnd_4digit_num = random.randrange(start=0, stop=10000, step=1)
        
        ext_name = 'MP4'

        # the first file looks like a normal file
        filename = 'GOPR{0:04d}.{1}'.format(rnd_4digit_num, ext_name)
        rnd_chap_list.append(filename)

        max_chap = 10
        number_of_sub_chap = random.randrange(start=1, stop=max_chap+1, step=1)
        
        
        for jj in range(number_of_sub_chap):
            
            # All the other chapter have the same last digit number
            filename = 'GP{0:02d}{1:04d}.{2}'.format(jj, rnd_4digit_num, ext_name)
            rnd_chap_list.append(filename)
    
    return rnd_chap_list


def gen_rnd_burst_loop_list(number_of_files=10):
    """ Generate a random filename list for burst mode.
    
    Returns
    -------
    list
        a list with random and valid GoPro string names for videos or photos 
        in burst mode.
    """
    rnd_burst_loop_list = []
    
    for ii in range(number_of_files):
        
        # the number 10000 is not include in the list.
        rnd_4digit_num = random.randrange(start=0, stop=10000, step=1)
        
        # select randomly MP4 or JPG files.bursr
        if bool(random.randrange(0,2,1)):
            ext_name = 'MP4'
        else:
            ext_name = 'JPG'
        
        max_chap = 10
        number_of_bursts = random.randrange(start=1, stop=max_chap+1, step=1)
        
        offset = random.randrange(start=0, stop=1000-max_chap, step=1)
        
        for jj in range(number_of_bursts):
            
        
            filename = 'G{0:03}{1:04d}.{2}'.format(offset+jj, rnd_4digit_num, ext_name)
            # pad with zeros if number is smaller.
        
            rnd_burst_loop_list.append(filename)
    
    return rnd_burst_loop_list


def gen_rnd_3d_list(number_of_files=10):
    """ Generate a random filename list for 3D mode.
    
    Returns
    -------
    list
        a list with random and valid GoPro string names for videos or photos 
        in 3D mode.
    """
    
    
    #TODO: make a function to simulate a list with 3d entries.
    rnd_3d_list = []
    
    for ii in range(number_of_files):
        
        # the number 10000 is not include in the list.
        rnd_4digit_num = random.randrange(start=0, stop=10000, step=1)
        
        # select randomly MP4 or JPG files.bursr
        if bool(random.randrange(0,2,1)):
            ext_name = 'MP4'
        else:
            ext_name = 'JPG'
        
        
        filename_r = '3D_R{0:04}.{1}'.format(rnd_4digit_num, ext_name)
        filename_l = '3D_L{0:04}.{1}'.format(rnd_4digit_num, ext_name)
        
        rnd_3d_list.append(filename_r)
        rnd_3d_list.append(filename_l)
            
    return rnd_3d_list


def gen_rnd_mix_list(num_of_files=10):
    
    filelist = gen_rnd_file_list(num_of_files)
    filelist.extend(gen_rnd_chap_list(num_of_files))
    filelist.extend(gen_rnd_burst_loop_list(num_of_files))
    filelist.extend(gen_rnd_3d_list(num_of_files))

    # in place randomization of filelist
    random.shuffle(filelist)
    
    return filelist

    

# Random file list generation to test the find and sort algorithm
# =============================================================================


def create_sorted_lists(filelist):
    """ Main logic to sort a given filelist into
    
    Parameters
    ----------
    
    Returns
    -------
    (dict_1, dict_2, dict_3, list_1, list_2)
        with the following meaning:
            
        dict_1: chap_vid_group_dict, the keys of the dict correspond to the 
                file number <zzzz>, which relates all the chapters to a group.
                The values are a list of strings which belong to the group.
        dict_2: burst_time_lapsed_dict, they keys
        dict_3: record_3d_dict, the keys of the dict correspond to the 
        list4: single_element_list, 
        list5: filelist
            
        
        chap_vid_group_dict, burst_time_lapsed_dict, record_3d_dict, single_element_list, filelist
            
    
    
    Further description
    -------------------
    
    This logic applies to Camera Models: 
        HD HERO2, HERO3, HERO3+, HERO (2014), HERO Session, HERO4, 
        HERO5 Black, HERO5 Session.
        
    1. The Chaptered Video becomes

        GP<xx><zzzz>.MP4  ===> <YYYY>-<MM>-<DD>_<hh>H-<mm>m-<ss>s_<xx>_<zzzz>.MP4

        Note that the first part of such series will be translated as

        GP<xx><zzzz>.<ext> ===> <YYYY>-<MM>-<DD>_<hh>H-<mm>m-<ss>s_000_<zzzz>.<ext>

    2. Burst, time-lapsed pictures or looping videos become

        G<yyy><zzzz>.<ext>  ===> <YYYY>-<MM>-<DD>_<hh>H-<mm>m-<ss>s_<yyy>_<zzzz>.<ext>

    3. 3d videos or photos become
    
        3D_<D><zzzz>.<ext> ===> <YYYY>-<MM>-<DD>_<hh>H-<mm>m-<ss>s_<zzzz>_<D>.<ext>

    4. single photos and videos become
    
        GOPR<zzzz>.<ext> ===> <YYYY>-<MM>-<DD>_<hh>H-<mm>m-<ss>s_<zzzz>.<ext>



    The following filename descripton are used:


        <ext>       placeholder for fileextentiom MP4, mp4, JPG or jpg 
        <xx>        placeholder for xx chapternumber
        <yyy>       placeholder for yyy burst number
        <zzzz>      placeholder for zzzz file number
        <D>         placeholder for direction, R or L in the 3d record
        <YYYY>      year placeholder
        <MM>        month placeholder
        <DD>        day placeholder
        <hh>        hour placeholder in 24h notation
        <mm>        minutes placeholder
        <ss>        second placeholder  
        
    """

    chap_vid_group_dict = {}
    single_element_list = []
    burst_time_lapsed_dict = {}
    record_3d_dict = {}

    # check at first chaptered videos:
    # ================================

    filelist, chap_vid_group_dict = find_chaptered_videos(filelist, chap_vid_group_dict)

    # extract now the burst/time-lapse/looping items:
    # ===============================================

    filelist, burst_time_lapsed_dict = map_burst_items(filelist, burst_time_lapsed_dict)

    # extract now the 3D recordings:
    # ==============================

    filelist, record_3d_dict = find_3d_records(filelist, record_3d_dict)

    # finally, extract the single video/photos:
    #==========================================

    filelist, single_element_list = find_single_items(filelist, single_element_list)
    
    # return also the list of the remaining, unextracted files

    return chap_vid_group_dict, burst_time_lapsed_dict, record_3d_dict, single_element_list, filelist


def search_and_rename(filelist):
    
    
    chap_vid_group_dict = {}
    single_element_list = []
    burst_time_lapsed_dict = {}
    record_3d_dict = {}
    
    rename_pattern_list = []

    # check at first chaptered videos:
    # ================================

    filelist, chap_vid_group_dict = find_chaptered_videos(filelist, chap_vid_group_dict)
    rename_pattern_list = map_chaptered_videos(chap_vid_group_dict, rename_pattern_list)

    # extract now the burst/time-lapse/looping items:
    # ===============================================

    filelist, burst_time_lapsed_dict = find_burst_items(filelist, burst_time_lapsed_dict)
    rename_pattern_list = map_burst_items(burst_time_lapsed_dict, rename_pattern_list)
    
    # extract now the 3D recordings:
    # ==============================

    filelist, record_3d_dict = find_3d_records(filelist, record_3d_dict)
    rename_pattern_list = map_3d_records(record_3d_dict, rename_pattern_list)
    
    # finally, extract the single video/photos:
    #==========================================

    filelist, single_element_list = find_single_items(filelist, single_element_list)
    rename_pattern_list = map_single_items(single_element_list, rename_pattern_list)
     
    # return also the list of the remaining, unextracted files
    
    return rename_pattern_list


# =============================================================================
# Indiviuduell finding algorithms

def find_chaptered_videos(filelist, chap_vid_group_dict={}):
    
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
    
    return filelist, chap_vid_group_dict


def find_burst_items(filelist, burst_time_lapsed_dict={}):
    
    # need to reverse the iteration prozess to remove entries while stepping
    for entry in reversed(filelist):

        match = re.match('G(\d{3})(\d{4})(\..*)', entry)
        
        if match:
            group_number = match.group(1)
            #print('group_number: ', group_number)
            
            if burst_time_lapsed_dict.get(group_number) is None:
                #print('create new dict entry:', entry)
                
                burst_time_lapsed_dict[group_number] = [entry]
            else:
                #print('insert entry in dict:', entry)
                
                # since the element 'entry' is iterated
                # reversely, it has to be appened at first place
                burst_time_lapsed_dict[group_number].insert(0, entry)
                
            filelist.remove(entry)
    
    return filelist, burst_time_lapsed_dict
    
def find_3d_records(filelist, record_3d_dict={}):
    
    # need to reverse the iteration prozess to remove entries while stepping
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

    
    return filelist, record_3d_dict

def find_single_items(filelist, single_element_list=[]):
    
    for entry in reversed(filelist):
        match = re.match('GOPR(\d{4})(\..*)', entry)
        if match:
            single_element_list.insert(0, entry)
            
            filelist.remove(entry)
    
    return filelist, single_element_list

# Indiviuduell finding algorithms
# =============================================================================


# =============================================================================
# Indiviuduell mapping algorithms

def map_chaptered_videos(chap_vid_group_dict, chap_vid_map_list=[]):
    """
        1. The Chaptered Video becomes

        GP<xx><zzzz>.MP4  ===> <YYYY>-<MM>-<DD>_<hh>h-<mm>m-<ss>s_<xx>_<zzzz>.MP4
        
        Note that the first part of such series will be translated as

        GOPR<zzzz>.<ext> ===> <YYYY>-<MM>-<DD>_<hh>H-<mm>m-<ss>s_00_<zzzz>.<ext>
    """
    
    
    for entry in chap_vid_group_dict:
        
        for chap_name in chap_vid_group_dict[entry]:
            
            match = re.match('GP(\d{2})(\d{4})(\..*)', chap_name)
            match_start_file = re.match('GOPR(\d{4})(\..*)', chap_name)
            
            if match:
                date_string = '{0}_{1}_{2}{3}'.format(get_date_taken(chap_name), 
                                                      match.group(1),
                                                      match.group(2),
                                                      match.group(3))
                # make a file list map to what the file should be renamed
                chap_vid_map_list.append([chap_name, date_string])
                
            elif match_start_file:
                
                date_string = '{0}_00_{1}{2}'.format(get_date_taken(chap_name), 
                                                      match.group(1),
                                                      match.group(2))
                # make a file list map to what the file should be renamed
                chap_vid_map_list.append([chap_name, date_string])                
                
            else:
                print('First file of chaptered videos does not exist.')
#                raise Exception('First file of chaptered videos does not' 
#                                'exist.')
                
    
    return chap_vid_map_list


def map_burst_items(burst_time_lapsed_dict, burst_map_list=[]):
    """
    2. Burst, time-lapsed pictures or looping videos become

        G<yyy><zzzz>.<ext>  ===> <YYYY>-<MM>-<DD>_<hh>H-<mm>m-<ss>s_<yyy>_<zzzz>.<ext>

    """
    
    
    for entry in burst_time_lapsed_dict:
        
        for burst_name in burst_time_lapsed_dict[entry]:
            
            match = re.match('G(\d{3})(\d{4})(\..*)', burst_name)
            
            date_string = '{0}_{1}_{2}{3}'.format(get_date_taken(burst_name), 
                                                  match.group(1),
                                                  match.group(2),
                                                  match.group(3))
            
            # make a file list map to what the file should be renamed
            burst_map_list.append([burst_name, date_string])
    
    return burst_map_list


def map_3d_records(record_3d_dict, record_3d_map_list=[]):
    """
        3. 3d videos or photos become
    
        3D_<D><zzzz>.<ext> ===> <YYYY>-<MM>-<DD>_<hh>H-<mm>m-<ss>s_<zzzz>_<D>.<ext>
    """
    
    for entry in record_3d_dict:
        
        for name_3d in record_3d_dict[entry]:
            
            match = re.match('3D_(R|L)(\d{4})(\..*)', name_3d)
            
            date_string = '{0}_{1}_{2}{3}'.format(get_date_taken(name_3d), 
                                                  match.group(2),
                                                  match.group(1),
                                                  match.group(3))
            
            record_3d_map_list.append([name_3d, date_string])
    
    return record_3d_map_list


def map_single_items(single_item_list, single_item_map_list=[]):
    """ 
        4. single photos and videos become
    
        GOPR<zzzz>.<ext> ===> <YYYY>-<MM>-<DD>_<hh>H-<mm>m-<ss>s_<zzzz>.<ext>
    
    """
    
    for entry in single_item_list:
        match = re.match('GOPR(\d{4})(\..*)', entry)
        date_string = '{0}_{1}{2}'.format(get_date_taken(entry), 
                                              match.group(1),
                                              match.group(2))
        
        single_item_map_list.append([entry, date_string])
        
    return single_item_map_list 
        


# Indiviuduell mapping algorithms
# =============================================================================



def get_creation_date(filepath):
    timestamp = os.path.getctime(filepath)
    return datetime.datetime.fromtimestamp(timestamp)

def format_timestamp(filepath):
    datetime_obj = get_creation_date(filepath)
    return datetime_obj.strftime('%Y-%m-%d_%Hh%Mm%Ss')

def copy_with_meta(old_filename, new_filename):
    return shutil.copy2(old_filename, new_filename) 

def rename_filename(pattern_map_list):
    """ A rename method. """
    try:
        os.rename(pattern_map_list[0], pattern_map_list[1])
    except Exception as exp:
        print('Cannot rename file "{0}" ==> "{1}". The following error '
              'occured: {2}'.format(pattern_map_list[0],
                                    pattern_map_list[1],
                                    exp))

def get_date_taken(path):
    
    extension = path[-3:].lower() # either MP4 or JPG
    
    if extension == 'mp4':
        res = get_creation_date_vid(path)
    elif extension == 'jpg':
        res = get_creation_date_img(path)
    else:
        raise Exception('What is this for an extension??? "{0}" was given!'.format(extension))
        
    return res
    


def get_creation_date_img(path):
    
    creation_date = Image.open(path)._getexif()[36867]
    
    creation_date_dt = datetime.datetime.strptime(creation_date, '%Y:%m:%d %H:%M:%S')
    
    return creation_date_dt.strftime('%Y-%m-%d_%Hh%Mm%Ss')


def get_creation_date_vid(path):
    """
    ffprobe GOPR8685.MP4 -v quiet -print_format json -show_streams > info.txt
    """
    
    command = ['ffprobe', path, '-v', 'quiet', '-print_format', 'json',
               '-show_streams']
    ffmpeg = subprocess.Popen(command, stderr=subprocess.PIPE, 
                              stdout=subprocess.PIPE)
    out, err = ffmpeg.communicate()
    
    meta_dict = json.loads(out.decode())
    
    # it is enough to look at the first stream.
    raw_date = meta_dict['streams'][0]['tags']['creation_time']
    
    # in the first part is the date and the time:
    striped_date = raw_date[0:19]
    
    creation_date_dt = datetime.datetime.strptime(striped_date, '%Y-%m-%dT%H:%M:%S')
    
    return creation_date_dt.strftime('%Y-%m-%d_%Hh%Mm%Ss')


def get_all_files_in_folder(path):
    
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

def extract_video_information(path):
    """
    ffprobe <filename> -v quiet -print_format json -show_streams > info.txt
    """
    
    command = ['ffprobe', path, '-v', 'quiet', '-print_format', 'json',
               '-show_streams']
    
    ffmpeg = subprocess.Popen(command, stderr=subprocess.PIPE, 
                              stdout=subprocess.PIPE)
    out, err = ffmpeg.communicate()
    
    return out.decode()


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
#    print(gen_rnd_burst_loop_list())
    
    folderpath = os.path.abspath(r'C:\Users\AlexS\Desktop\test2')
    os.chdir(folderpath)
    print(os.path.abspath(os.curdir))
    filelist = get_all_files_in_folder(folderpath)
    print(filelist)
    
    rename_pattern_list = search_and_rename(filelist)
    
    for rename_pattern in rename_pattern_list:
        rename_filename(rename_pattern)
    
    
    

    

    
    