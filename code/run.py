#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 17:15:07 2020

@author: sophia
"""

from __future__ import print_function
# To begin using librosa we need to import it, and other tools such as matplotlib and numpy
from pylab import *
import librosa             # The librosa library
import librosa.display     # librosa's display module (for plotting features)
import IPython.display     # IPython's display module (for in-line audio)
import matplotlib.pyplot as plt # matplotlib plotting functions
import matplotlib.style as ms   # plotting style
import numpy as np              # numpy numerical functions
ms.use('seaborn-muted')         # fancy plot designs

import pretty_midi

from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox







def key_library(key):
    library={"C": 12,"D":14, "E":16, "F": 17, "G":19, "A": 21, "B": 23}
    return library[key]

def major_library(key_name):
    library={"major":[0,2,4,5,7,9,11],"natural_minor":[0,2,3,5,7,8,10], \
             "harmonic_minor":[0,2,3,5,7,8,11],"melodic_minor":[0,2,3,5,7,9,11], \
             "Chinese":[0,2,4,7,9],"Japanese": [0,2,3,7,8]}
    return library[key_name]


def create_mainlib(width,key_scale,colors):
    main_lib={}
    for i in range(0,len(colors)):
        main_lib[colors[i]] = {} #create_lib(width,key_scale)
    return main_lib

def output_note(lib):
    List=[]
    for key in lib:
        if lib[key] > 20:
            List.append(key)
    return List
    
def spectrum_to_wave(key_scale,Tuple,width,colors):    # x->time y->frequency
    
    #create empty library
    main_lib=create_mainlib(width, key_scale, colors)
    
    #store all elements  
    for item in Tuple:
        x=item[0]//10
        for i in range(-5,5):
            y=item[1]
            y+=i
            y//=10
            if (x,y) in main_lib[item[2]]:
                main_lib[item[2]][(x,y)] += 1
            else:
                main_lib[item[2]][(x,y)] = 0
    print("main_lib",main_lib)
    print()
    #remove empty box
    notes={}
    for key in main_lib:
        result=output_note(main_lib[key])
        notes[key]=result
     
    return notes


def note(key_note,key_scale,note):
    new_note=[]
    for i in range(0,len(note)):
        new_note.append((note[i][0],key_note + (note[i][1]//len(key_scale))*12 \
                         + key_scale[note[i][1]%len(key_scale)]))
    return new_note

def chord_library(key_name):
    pass
def add_chord(key_note, key_chord, note):
    pass


#(x,y,color)
def collect_notes(Tuple,key_letter,key_name,width,colors):
    #fetch Tuple (notes)
    #fetch key_letter (A,B...)
    #fetch key_name (major,minor...)
    #fetch width (pen size)
    #fetch colors (["red","blue"])
    key_note=key_library(key_letter)
    key_scale=major_library(key_name)

    note_digit=spectrum_to_wave(key_scale,Tuple,width,colors)
    #note_digit={'green': [(39, 21), (40, 21), (41, 21), (56, 21)]}
    #print("note_digit",note_digit)
    notes={}
    print("note_digit",note_digit)
    for item in note_digit:
        notes[item]=note(key_note,key_scale,note_digit[item])
    return notes




def color_instrument(color):
    lib = {"green":"Cello","brown": "Cello", "orange": "Violin", "black": "Acoustic Grand Piano", "purple": "Flute"}
    return lib[color]

def midi(notes,velocity,time_list,instrument):
    
    
    cello_program = pretty_midi.instrument_name_to_program(instrument)
    cello = pretty_midi.Instrument(program=cello_program)
    i=1


    '''
    while not i==len(notes)-3:
        print(i)
        while notes[i] == notes[i-1] and time[i]==time[i-1]+1:
            
            print("notes",notes)
            notes.remove(notes[i])
            time.remove(time[i])
        i+=1
    '''
    end_time_list=[]
    for i in range(0,len(notes)-1):
        if not time_list[i+1]-time_list[i]>4:
            end_time_list.append(time_list[i+1])
        else:
            end_time_list.append(time_list[i]+4)
    end_time_list.append(time_list[len(time_list)-1]+4)
    i=0
    
    while i<len(notes)-4:
        
        while notes[i]==notes[i+1] and end_time_list[i]==time_list[i+1]:
            #print(notes)
            #print("time", time_list)
            #print("end_time",end_time_list)
            notes.remove(notes[i+1])
            time_list.remove(time_list[i+1])
            end_time_list[i]=end_time_list[i+1]
            end_time_list.remove(end_time_list[i+1])
            if i>=len(notes)-1:
                break
       
        '''
        while notes[i]==notes[i+2] and end_time_list[i]==time_list[i+2]:
            #print(notes)
            #print("time", time_list)
            #print("end_time",end_time_list)
            notes.remove(notes[i+2])
            time_list.remove(time_list[i+2])
            end_time_list[i]=end_time_list[i+2]
            end_time_list.remove(end_time_list[i+2])
            if i>=len(notes)-2:
                break
        '''
        i+=1
    

    for i in range(0,len(notes)-1):
        
        start_time=time_list[i]/2
        end_time=end_time_list[i]/2
        note = pretty_midi.Note(velocity=velocity, pitch=notes[i], start=start_time, end=end_time)
        cello.notes.append(note)
    last_note=pretty_midi.Note(velocity=velocity, pitch=notes[len(notes)-1],start=time_list[len(time_list)-1]/2,end=(time_list[len(time_list)-1]+4)/2)
    cello.notes.append(last_note)
    return cello

def output_midi(notes,velocity):
    music = pretty_midi.PrettyMIDI()
    
    
    for item in notes:
        time=[]
        note_list=[]
        if len(notes[item])==0:
            continue
        for x in notes[item]:
            time.append(x[0])
            note_list.append(x[1])
            
        instrument=color_instrument(item)
        print(instrument,note_list)
        instrument_program=midi(note_list,velocity,time,instrument)
        music.instruments.append(instrument_program)
    music.write('music.mid')




def main(Tuple,key_letter,key_name):
    '''
    Tuple=[(4, 336, 'black'), (6, 336, 'black'), (5, 336, 'black'), (10, 336, 'black'), (7, 336, 'black'), (8, 336, 'black'), (9, 336, 'black'), (14, 336, 'black'), (11, 336, 'black'), (12, 336, 'black'), (13, 336, 'black'), (28, 336, 'black'), (15, 336, 'black'), (16, 336, 'black'), (17, 336, 'black'), (18, 336, 'black'), (19, 336, 'black'), (20, 336, 'black'), (21, 336, 'black'), (22, 336, 'black'), (23, 336, 'black'), (24, 336, 'black'), (25, 336, 'black'), (26, 336, 'black'), (27, 336, 'black'), (44, 336, 'black'), (29, 336, 'black'), (30, 336, 'black'), (31, 336, 'black'), (32, 336, 'black'), (33, 336, 'black'), (34, 336, 'black'), (35, 336, 'black'), (36, 336, 'black'), (37, 336, 'black'), (38, 336, 'black'), (39, 336, 'black'), (40, 336, 'black'), (41, 336, 'black'), (42, 336, 'black'), (43, 336, 'black'), (60, 336, 'black'), (45, 336, 'black'), (46, 336, 'black'), (47, 336, 'black'), (48, 336, 'black'), (49, 336, 'black'), (50, 336, 'black'), (51, 336, 'black'), (52, 336, 'black'), (53, 336, 'black'), (54, 336, 'black'), (55, 336, 'black'), (56, 336, 'black'), (57, 336, 'black'), (58, 336, 'black'), (59, 336, 'black'), (76, 336, 'black'), (61, 336, 'black'), (62, 336, 'black'), (63, 336, 'black'), (64, 336, 'black'), (65, 336, 'black'), (66, 336, 'black'), (67, 336, 'black'), (68, 336, 'black'), (69, 336, 'black'), (70, 336, 'black'), (71, 336, 'black'), (72, 336, 'black'), (73, 336, 'black'), (74, 336, 'black'), (75, 336, 'black'), (90, 336, 'black'), (77, 336, 'black'), (78, 336, 'black'), (79, 336, 'black'), (80, 336, 'black'), (81, 336, 'black'), (82, 336, 'black'), (83, 336, 'black'), (84, 336, 'black'), (85, 336, 'black'), (86, 336, 'black'), (87, 336, 'black'), (88, 336, 'black'), (89, 336, 'black'), (105, 336, 'black'), (91, 336, 'black'), (92, 336, 'black'), (93, 336, 'black'), (94, 336, 'black'), (95, 336, 'black'), (96, 336, 'black'), (97, 336, 'black'), (98, 336, 'black'), (99, 336, 'black'), (100, 336, 'black'), (101, 336, 'black'), (102, 336, 'black'), (103, 336, 'black'), (104, 336, 'black'), (119, 336, 'black'), (106, 336, 'black'), (107, 336, 'black'), (108, 336, 'black'), (109, 336, 'black'), (110, 336, 'black'), (111, 336, 'black'), (112, 336, 'black'), (113, 336, 'black'), (114, 336, 'black'), (115, 336, 'black'), (116, 336, 'black'), (117, 336, 'black'), (118, 336, 'black'), (136, 336, 'black'), (120, 336, 'black'), (121, 336, 'black'), (122, 336, 'black'), (123, 336, 'black'), (124, 336, 'black'), (125, 336, 'black'), (126, 336, 'black'), (127, 336, 'black'), (128, 336, 'black'), (129, 336, 'black'), (130, 336, 'black'), (131, 336, 'black'), (132, 336, 'black'), (133, 336, 'black'), (134, 336, 'black'), (135, 336, 'black'), (151, 336, 'black'), (137, 336, 'black'), (138, 336, 'black'), (139, 336, 'black'), (140, 336, 'black'), (141, 336, 'black'), (142, 336, 'black'), (143, 336, 'black'), (144, 336, 'black'), (145, 336, 'black'), (146, 336, 'black'), (147, 336, 'black'), (148, 336, 'black'), (149, 336, 'black'), (150, 336, 'black'), (167, 336, 'black'), (152, 336, 'black'), (153, 336, 'black'), (154, 336, 'black'), (155, 336, 'black'), (156, 336, 'black'), (157, 336, 'black'), (158, 336, 'black'), (159, 336, 'black'), (160, 336, 'black'), (161, 336, 'black'), (162, 336, 'black'), (163, 336, 'black'), (164, 336, 'black'), (165, 336, 'black'), (166, 336, 'black'), (183, 336, 'black'), (168, 336, 'black'), (169, 336, 'black'), (170, 336, 'black'), (171, 336, 'black'), (172, 336, 'black'), (173, 336, 'black'), (174, 336, 'black'), (175, 336, 'black'), (176, 336, 'black'), (177, 336, 'black'), (178, 336, 'black'), (179, 336, 'black'), (180, 336, 'black'), (181, 336, 'black'), (182, 336, 'black'), (201, 336, 'black'), (184, 336, 'black'), (185, 336, 'black'), (186, 336, 'black'), (187, 336, 'black'), (188, 336, 'black'), (189, 336, 'black'), (190, 336, 'black'), (191, 336, 'black'), (192, 336, 'black'), (193, 336, 'black'), (194, 336, 'black'), (195, 336, 'black'), (196, 336, 'black'), (197, 336, 'black'), (198, 336, 'black'), (199, 336, 'black'), (200, 336, 'black'), (216, 336, 'black'), (202, 336, 'black'), (203, 336, 'black'), (204, 336, 'black'), (205, 336, 'black'), (206, 336, 'black'), (207, 336, 'black'), (208, 336, 'black'), (209, 336, 'black'), (210, 336, 'black'), (211, 336, 'black'), (212, 336, 'black'), (213, 336, 'black'), (214, 336, 'black'), (215, 336, 'black'), (233, 336, 'black'), (217, 336, 'black'), (218, 336, 'black'), (219, 336, 'black'), (220, 336, 'black'), (221, 336, 'black'), (222, 336, 'black'), (223, 336, 'black'), (224, 336, 'black'), (225, 336, 'black'), (226, 336, 'black'), (227, 336, 'black'), (228, 336, 'black'), (229, 336, 'black'), (230, 336, 'black'), (231, 336, 'black'), (232, 336, 'black'), (252, 337, 'black'), (271, 339, 'black'), (281, 341, 'black'), (291, 342, 'black'), (295, 344, 'black'), (301, 346, 'black'), (234, 225, 'black'), (236, 225, 'black'), (235, 225, 'black'), (238, 225, 'black'), (237, 225, 'black'), (240, 225, 'black'), (239, 225, 'black'), (241, 225, 'black'), (245, 225, 'black'), (242, 225, 'black'), (243, 225, 'black'), (244, 225, 'black'), (247, 225, 'black'), (246, 225, 'black'), (249, 225, 'black'), (248, 225, 'black'), (252, 225, 'black'), (250, 225, 'black'), (251, 225, 'black'), (255, 226, 'black'), (256, 226, 'black'), (257, 226, 'black'), (259, 226, 'black'), (258, 226, 'black'), (265, 228, 'black'), (274, 229, 'black'), (283, 232, 'black'), (293, 234, 'black'), (303, 237, 'black'), (313, 240, 'black'), (323, 244, 'black'), (334, 247, 'black'), (346, 251, 'black'), (356, 255, 'black'), (368, 258, 'black'), (380, 260, 'black'), (397, 262, 'black'), (413, 266, 'black'), (433, 269, 'black'), (466, 273, 'black'), (489, 277, 'black'), (534, 281, 'black'), (576, 286, 'black'), (625, 293, 'black'), (641, 297, 'black'), (675, 302, 'black'), (683, 303, 'black'), (696, 304, 'black'), (698, 305, 'black'), (701, 305, 'black'), (699, 305, 'black'), (700, 305, 'black'), (701, 306, 'black'), (235, 433, 'purple'), (238, 433, 'purple'), (236, 433, 'purple'), (237, 433, 'purple'), (243, 433, 'purple'), (239, 433, 'purple'), (240, 433, 'purple'), (241, 433, 'purple'), (242, 433, 'purple'), (262, 433, 'purple'), (244, 433, 'purple'), (245, 433, 'purple'), (246, 433, 'purple'), (247, 433, 'purple'), (248, 433, 'purple'), (249, 433, 'purple'), (250, 433, 'purple'), (251, 433, 'purple'), (252, 433, 'purple'), (253, 433, 'purple'), (254, 433, 'purple'), (255, 433, 'purple'), (256, 433, 'purple'), (257, 433, 'purple'), (258, 433, 'purple'), (259, 433, 'purple'), (260, 433, 'purple'), (261, 433, 'purple'), (287, 433, 'purple'), (263, 433, 'purple'), (264, 433, 'purple'), (265, 433, 'purple'), (266, 433, 'purple'), (267, 433, 'purple'), (268, 433, 'purple'), (269, 433, 'purple'), (270, 433, 'purple'), (271, 433, 'purple'), (272, 433, 'purple'), (273, 433, 'purple'), (274, 433, 'purple'), (275, 433, 'purple'), (276, 433, 'purple'), (277, 433, 'purple'), (278, 433, 'purple'), (279, 433, 'purple'), (280, 433, 'purple'), (281, 433, 'purple'), (282, 433, 'purple'), (283, 433, 'purple'), (284, 433, 'purple'), (285, 433, 'purple'), (286, 433, 'purple'), (305, 433, 'purple'), (288, 433, 'purple'), (289, 433, 'purple'), (290, 433, 'purple'), (291, 433, 'purple'), (292, 433, 'purple'), (293, 433, 'purple'), (294, 433, 'purple'), (295, 433, 'purple'), (296, 433, 'purple'), (297, 433, 'purple'), (298, 433, 'purple'), (299, 433, 'purple'), (300, 433, 'purple'), (301, 433, 'purple'), (302, 433, 'purple'), (303, 433, 'purple'), (304, 433, 'purple'), (348, 433, 'purple'), (306, 433, 'purple'), (307, 433, 'purple'), (308, 433, 'purple'), (309, 433, 'purple'), (310, 433, 'purple'), (311, 433, 'purple'), (312, 433, 'purple'), (313, 433, 'purple'), (314, 433, 'purple'), (315, 433, 'purple'), (316, 433, 'purple'), (317, 433, 'purple'), (318, 433, 'purple'), (319, 433, 'purple'), (320, 433, 'purple'), (321, 433, 'purple'), (322, 433, 'purple'), (323, 433, 'purple'), (324, 433, 'purple'), (325, 433, 'purple'), (326, 433, 'purple'), (327, 433, 'purple'), (328, 433, 'purple'), (329, 433, 'purple'), (330, 433, 'purple'), (331, 433, 'purple'), (332, 433, 'purple'), (333, 433, 'purple'), (334, 433, 'purple'), (335, 433, 'purple'), (336, 433, 'purple'), (337, 433, 'purple'), (338, 433, 'purple'), (339, 433, 'purple'), (340, 433, 'purple'), (341, 433, 'purple'), (342, 433, 'purple'), (343, 433, 'purple'), (344, 433, 'purple'), (345, 433, 'purple'), (346, 433, 'purple'), (347, 433, 'purple'), (371, 433, 'purple'), (349, 433, 'purple'), (350, 433, 'purple'), (351, 433, 'purple'), (352, 433, 'purple'), (353, 433, 'purple'), (354, 433, 'purple'), (355, 433, 'purple'), (356, 433, 'purple'), (357, 433, 'purple'), (358, 433, 'purple'), (359, 433, 'purple'), (360, 433, 'purple'), (361, 433, 'purple'), (362, 433, 'purple'), (363, 433, 'purple'), (364, 433, 'purple'), (365, 433, 'purple'), (366, 433, 'purple'), (367, 433, 'purple'), (368, 433, 'purple'), (369, 433, 'purple'), (370, 433, 'purple'), (400, 433, 'purple'), (372, 433, 'purple'), (373, 433, 'purple'), (374, 433, 'purple'), (375, 433, 'purple'), (376, 433, 'purple'), (377, 433, 'purple'), (378, 433, 'purple'), (379, 433, 'purple'), (380, 433, 'purple'), (381, 433, 'purple'), (382, 433, 'purple'), (383, 433, 'purple'), (384, 433, 'purple'), (385, 433, 'purple'), (386, 433, 'purple'), (387, 433, 'purple'), (388, 433, 'purple'), (389, 433, 'purple'), (390, 433, 'purple'), (391, 433, 'purple'), (392, 433, 'purple'), (393, 433, 'purple'), (394, 433, 'purple'), (395, 433, 'purple'), (396, 433, 'purple'), (397, 433, 'purple'), (398, 433, 'purple'), (399, 433, 'purple'), (420, 433, 'purple'), (401, 433, 'purple'), (402, 433, 'purple'), (403, 433, 'purple'), (404, 433, 'purple'), (405, 433, 'purple'), (406, 433, 'purple'), (407, 433, 'purple'), (408, 433, 'purple'), (409, 433, 'purple'), (410, 433, 'purple'), (411, 433, 'purple'), (412, 433, 'purple'), (413, 433, 'purple'), (414, 433, 'purple'), (415, 433, 'purple'), (416, 433, 'purple'), (417, 433, 'purple'), (418, 433, 'purple'), (419, 433, 'purple'), (429, 433, 'purple'), (421, 433, 'purple'), (422, 433, 'purple'), (423, 433, 'purple'), (424, 433, 'purple'), (425, 433, 'purple'), (426, 433, 'purple'), (427, 433, 'purple'), (428, 433, 'purple'), (435, 433, 'purple'), (430, 433, 'purple'), (431, 433, 'purple'), (432, 433, 'purple'), (433, 433, 'purple'), (434, 433, 'purple'), (438, 433, 'purple'), (436, 433, 'purple'), (437, 433, 'purple'), (501, 462, 'purple'), (508, 462, 'purple'), (502, 462, 'purple'), (503, 462, 'purple'), (504, 462, 'purple'), (505, 462, 'purple'), (506, 462, 'purple'), (507, 462, 'purple'), (521, 462, 'purple'), (509, 462, 'purple'), (510, 462, 'purple'), (511, 462, 'purple'), (512, 462, 'purple'), (513, 462, 'purple'), (514, 462, 'purple'), (515, 462, 'purple'), (516, 462, 'purple'), (517, 462, 'purple'), (518, 462, 'purple'), (519, 462, 'purple'), (520, 462, 'purple'), (559, 462, 'purple'), (522, 462, 'purple'), (523, 462, 'purple'), (524, 462, 'purple'), (525, 462, 'purple'), (526, 462, 'purple'), (527, 462, 'purple'), (528, 462, 'purple'), (529, 462, 'purple'), (530, 462, 'purple'), (531, 462, 'purple'), (532, 462, 'purple'), (533, 462, 'purple'), (534, 462, 'purple'), (535, 462, 'purple'), (536, 462, 'purple'), (537, 462, 'purple'), (538, 462, 'purple'), (539, 462, 'purple'), (540, 462, 'purple'), (541, 462, 'purple'), (542, 462, 'purple'), (543, 462, 'purple'), (544, 462, 'purple'), (545, 462, 'purple'), (546, 462, 'purple'), (547, 462, 'purple'), (548, 462, 'purple'), (549, 462, 'purple'), (550, 462, 'purple'), (551, 462, 'purple'), (552, 462, 'purple'), (553, 462, 'purple'), (554, 462, 'purple'), (555, 462, 'purple'), (556, 462, 'purple'), (557, 462, 'purple'), (558, 462, 'purple'), (678, 462, 'purple'), (560, 462, 'purple'), (561, 462, 'purple'), (562, 462, 'purple'), (563, 462, 'purple'), (564, 462, 'purple'), (565, 462, 'purple'), (566, 462, 'purple'), (567, 462, 'purple'), (568, 462, 'purple'), (569, 462, 'purple'), (570, 462, 'purple'), (571, 462, 'purple'), (572, 462, 'purple'), (573, 462, 'purple'), (574, 462, 'purple'), (575, 462, 'purple'), (576, 462, 'purple'), (577, 462, 'purple'), (578, 462, 'purple'), (579, 462, 'purple'), (580, 462, 'purple'), (581, 462, 'purple'), (582, 462, 'purple'), (583, 462, 'purple'), (584, 462, 'purple'), (585, 462, 'purple'), (586, 462, 'purple'), (587, 462, 'purple'), (588, 462, 'purple'), (589, 462, 'purple'), (590, 462, 'purple'), (591, 462, 'purple'), (592, 462, 'purple'), (593, 462, 'purple'), (594, 462, 'purple'), (595, 462, 'purple'), (596, 462, 'purple'), (597, 462, 'purple'), (598, 462, 'purple'), (599, 462, 'purple'), (600, 462, 'purple'), (601, 462, 'purple'), (602, 462, 'purple'), (603, 462, 'purple'), (604, 462, 'purple'), (605, 462, 'purple'), (606, 462, 'purple'), (607, 462, 'purple'), (608, 462, 'purple'), (609, 462, 'purple'), (610, 462, 'purple'), (611, 462, 'purple'), (612, 462, 'purple'), (613, 462, 'purple'), (614, 462, 'purple'), (615, 462, 'purple'), (616, 462, 'purple'), (617, 462, 'purple'), (618, 462, 'purple'), (619, 462, 'purple'), (620, 462, 'purple'), (621, 462, 'purple'), (622, 462, 'purple'), (623, 462, 'purple'), (624, 462, 'purple'), (625, 462, 'purple'), (626, 462, 'purple'), (627, 462, 'purple'), (628, 462, 'purple'), (629, 462, 'purple'), (630, 462, 'purple'), (631, 462, 'purple'), (632, 462, 'purple'), (633, 462, 'purple'), (634, 462, 'purple'), (635, 462, 'purple'), (636, 462, 'purple'), (637, 462, 'purple'), (638, 462, 'purple'), (639, 462, 'purple'), (640, 462, 'purple'), (641, 462, 'purple'), (642, 462, 'purple'), (643, 462, 'purple'), (644, 462, 'purple'), (645, 462, 'purple'), (646, 462, 'purple'), (647, 462, 'purple'), (648, 462, 'purple'), (649, 462, 'purple'), (650, 462, 'purple'), (651, 462, 'purple'), (652, 462, 'purple'), (653, 462, 'purple'), (654, 462, 'purple'), (655, 462, 'purple'), (656, 462, 'purple'), (657, 462, 'purple'), (658, 462, 'purple'), (659, 462, 'purple'), (660, 462, 'purple'), (661, 462, 'purple'), (662, 462, 'purple'), (663, 462, 'purple'), (664, 462, 'purple'), (665, 462, 'purple'), (666, 462, 'purple'), (667, 462, 'purple'), (668, 462, 'purple'), (669, 462, 'purple'), (670, 462, 'purple'), (671, 462, 'purple'), (672, 462, 'purple'), (673, 462, 'purple'), (674, 462, 'purple'), (675, 462, 'purple'), (676, 462, 'purple'), (677, 462, 'purple'), (752, 462, 'purple'), (679, 462, 'purple'), (680, 462, 'purple'), (681, 462, 'purple'), (682, 462, 'purple'), (683, 462, 'purple'), (684, 462, 'purple'), (685, 462, 'purple'), (686, 462, 'purple'), (687, 462, 'purple'), (688, 462, 'purple'), (689, 462, 'purple'), (690, 462, 'purple'), (691, 462, 'purple'), (692, 462, 'purple'), (693, 462, 'purple'), (694, 462, 'purple'), (695, 462, 'purple'), (696, 462, 'purple'), (697, 462, 'purple'), (698, 462, 'purple'), (699, 462, 'purple'), (700, 462, 'purple'), (701, 462, 'purple'), (702, 462, 'purple'), (703, 462, 'purple'), (704, 462, 'purple'), (705, 462, 'purple'), (706, 462, 'purple'), (707, 462, 'purple'), (708, 462, 'purple'), (709, 462, 'purple'), (710, 462, 'purple'), (711, 462, 'purple'), (712, 462, 'purple'), (713, 462, 'purple'), (714, 462, 'purple'), (715, 462, 'purple'), (716, 462, 'purple'), (717, 462, 'purple'), (718, 462, 'purple'), (719, 462, 'purple'), (720, 462, 'purple'), (721, 462, 'purple'), (722, 462, 'purple'), (723, 462, 'purple'), (724, 462, 'purple'), (725, 462, 'purple'), (726, 462, 'purple'), (727, 462, 'purple'), (728, 462, 'purple'), (729, 462, 'purple'), (730, 462, 'purple'), (731, 462, 'purple'), (732, 462, 'purple'), (733, 462, 'purple'), (734, 462, 'purple'), (735, 462, 'purple'), (736, 462, 'purple'), (737, 462, 'purple'), (738, 462, 'purple'), (739, 462, 'purple'), (740, 462, 'purple'), (741, 462, 'purple'), (742, 462, 'purple'), (743, 462, 'purple'), (744, 462, 'purple'), (745, 462, 'purple'), (746, 462, 'purple'), (747, 462, 'purple'), (748, 462, 'purple'), (749, 462, 'purple'), (750, 462, 'purple'), (751, 462, 'purple'), (790, 462, 'purple'), (753, 462, 'purple'), (754, 462, 'purple'), (755, 462, 'purple'), (756, 462, 'purple'), (757, 462, 'purple'), (758, 462, 'purple'), (759, 462, 'purple'), (760, 462, 'purple'), (761, 462, 'purple'), (762, 462, 'purple'), (763, 462, 'purple'), (764, 462, 'purple'), (765, 462, 'purple'), (766, 462, 'purple'), (767, 462, 'purple'), (768, 462, 'purple'), (769, 462, 'purple'), (770, 462, 'purple'), (771, 462, 'purple'), (772, 462, 'purple'), (773, 462, 'purple'), (774, 462, 'purple'), (775, 462, 'purple'), (776, 462, 'purple'), (777, 462, 'purple'), (778, 462, 'purple'), (779, 462, 'purple'), (780, 462, 'purple'), (781, 462, 'purple'), (782, 462, 'purple'), (783, 462, 'purple'), (784, 462, 'purple'), (785, 462, 'purple'), (786, 462, 'purple'), (787, 462, 'purple'), (788, 462, 'purple'), (789, 462, 'purple'), (825, 462, 'purple'), (791, 462, 'purple'), (792, 462, 'purple'), (793, 462, 'purple'), (794, 462, 'purple'), (795, 462, 'purple'), (796, 462, 'purple'), (797, 462, 'purple'), (798, 462, 'purple'), (799, 462, 'purple'), (800, 462, 'purple'), (801, 462, 'purple'), (802, 462, 'purple'), (803, 462, 'purple'), (804, 462, 'purple'), (805, 462, 'purple'), (806, 462, 'purple'), (807, 462, 'purple'), (808, 462, 'purple'), (809, 462, 'purple'), (810, 462, 'purple'), (811, 462, 'purple'), (812, 462, 'purple'), (813, 462, 'purple'), (814, 462, 'purple'), (815, 462, 'purple'), (816, 462, 'purple'), (817, 462, 'purple'), (818, 462, 'purple'), (819, 462, 'purple'), (820, 462, 'purple'), (821, 462, 'purple'), (822, 462, 'purple'), (823, 462, 'purple'), (824, 462, 'purple'), (841, 462, 'purple'), (826, 462, 'purple'), (827, 462, 'purple'), (828, 462, 'purple'), (829, 462, 'purple'), (830, 462, 'purple'), (831, 462, 'purple'), (832, 462, 'purple'), (833, 462, 'purple'), (834, 462, 'purple'), (835, 462, 'purple'), (836, 462, 'purple'), (837, 462, 'purple'), (838, 462, 'purple'), (839, 462, 'purple'), (840, 462, 'purple'), (846, 462, 'purple'), (842, 462, 'purple'), (843, 462, 'purple'), (844, 462, 'purple'), (845, 462, 'purple'), (504, 456, 'purple'), (505, 456, 'purple'), (506, 456, 'purple'), (507, 456, 'purple'), (508, 456, 'purple'), (509, 456, 'purple'), (510, 456, 'purple'), (511, 456, 'purple'), (512, 456, 'purple'), (514, 456, 'purple'), (513, 456, 'purple'), (516, 456, 'purple'), (515, 456, 'purple'), (517, 456, 'purple'), (518, 456, 'purple'), (519, 455, 'purple'), (520, 455, 'purple'), (521, 455, 'purple'), (522, 455, 'purple'), (523, 455, 'purple'), (525, 455, 'purple'), (524, 455, 'purple'), (527, 455, 'purple'), (526, 455, 'purple'), (530, 455, 'purple'), (528, 455, 'purple'), (529, 455, 'purple'), (532, 455, 'purple'), (531, 455, 'purple'), (535, 455, 'purple'), (533, 455, 'purple'), (534, 455, 'purple'), (538, 455, 'purple'), (536, 455, 'purple'), (537, 455, 'purple'), (540, 454, 'purple'), (543, 454, 'purple'), (541, 454, 'purple'), (542, 454, 'purple'), (546, 454, 'purple'), (544, 454, 'purple'), (545, 454, 'purple'), (548, 454, 'purple'), (547, 454, 'purple'), (551, 454, 'purple'), (549, 454, 'purple'), (550, 454, 'purple'), (554, 454, 'purple'), (552, 454, 'purple'), (553, 454, 'purple'), (555, 454, 'purple'), (557, 454, 'purple'), (556, 454, 'purple'), (558, 454, 'purple'), (560, 454, 'purple'), (559, 454, 'purple'), (563, 454, 'purple'), (561, 454, 'purple'), (562, 454, 'purple'), (565, 454, 'purple'), (564, 454, 'purple'), (567, 454, 'purple'), (566, 454, 'purple'), (569, 454, 'purple'), (568, 454, 'purple'), (571, 454, 'purple'), (570, 454, 'purple'), (573, 454, 'purple'), (572, 454, 'purple'), (574, 454, 'purple'), (576, 454, 'purple'), (575, 454, 'purple'), (577, 454, 'purple'), (579, 454, 'purple'), (578, 454, 'purple'), (580, 454, 'purple'), (581, 454, 'purple'), (582, 454, 'purple'), (583, 454, 'purple'), (585, 454, 'purple'), (584, 454, 'purple'), (586, 454, 'purple'), (588, 454, 'purple'), (587, 454, 'purple'), (590, 454, 'purple'), (589, 454, 'purple'), (591, 454, 'purple'), (593, 454, 'purple'), (592, 454, 'purple'), (595, 454, 'purple'), (594, 454, 'purple'), (596, 454, 'purple'), (597, 454, 'purple'), (596, 454, 'purple'), (638, 440, 'purple'), (643, 440, 'purple'), (639, 440, 'purple'), (640, 440, 'purple'), (641, 440, 'purple'), (642, 440, 'purple'), (650, 440, 'purple'), (644, 440, 'purple'), (645, 440, 'purple'), (646, 440, 'purple'), (647, 440, 'purple'), (648, 440, 'purple'), (649, 440, 'purple'), (659, 440, 'purple'), (651, 440, 'purple'), (652, 440, 'purple'), (653, 440, 'purple'), (654, 440, 'purple'), (655, 440, 'purple'), (656, 440, 'purple'), (657, 440, 'purple'), (658, 440, 'purple'), (692, 440, 'purple'), (660, 440, 'purple'), (661, 440, 'purple'), (662, 440, 'purple'), (663, 440, 'purple'), (664, 440, 'purple'), (665, 440, 'purple'), (666, 440, 'purple'), (667, 440, 'purple'), (668, 440, 'purple'), (669, 440, 'purple'), (670, 440, 'purple'), (671, 440, 'purple'), (672, 440, 'purple'), (673, 440, 'purple'), (674, 440, 'purple'), (675, 440, 'purple'), (676, 440, 'purple'), (677, 440, 'purple'), (678, 440, 'purple'), (679, 440, 'purple'), (680, 440, 'purple'), (681, 440, 'purple'), (682, 440, 'purple'), (683, 440, 'purple'), (684, 440, 'purple'), (685, 440, 'purple'), (686, 440, 'purple'), (687, 440, 'purple'), (688, 440, 'purple'), (689, 440, 'purple'), (690, 440, 'purple'), (691, 440, 'purple'), (732, 440, 'purple'), (693, 440, 'purple'), (694, 440, 'purple'), (695, 440, 'purple'), (696, 440, 'purple'), (697, 440, 'purple'), (698, 440, 'purple'), (699, 440, 'purple'), (700, 440, 'purple'), (701, 440, 'purple'), (702, 440, 'purple'), (703, 440, 'purple'), (704, 440, 'purple'), (705, 440, 'purple'), (706, 440, 'purple'), (707, 440, 'purple'), (708, 440, 'purple'), (709, 440, 'purple'), (710, 440, 'purple'), (711, 440, 'purple'), (712, 440, 'purple'), (713, 440, 'purple'), (714, 440, 'purple'), (715, 440, 'purple'), (716, 440, 'purple'), (717, 440, 'purple'), (718, 440, 'purple'), (719, 440, 'purple'), (720, 440, 'purple'), (721, 440, 'purple'), (722, 440, 'purple'), (723, 440, 'purple'), (724, 440, 'purple'), (725, 440, 'purple'), (726, 440, 'purple'), (727, 440, 'purple'), (728, 440, 'purple'), (729, 440, 'purple'), (730, 440, 'purple'), (731, 440, 'purple'), (755, 440, 'purple'), (733, 440, 'purple'), (734, 440, 'purple'), (735, 440, 'purple'), (736, 440, 'purple'), (737, 440, 'purple'), (738, 440, 'purple'), (739, 440, 'purple'), (740, 440, 'purple'), (741, 440, 'purple'), (742, 440, 'purple'), (743, 440, 'purple'), (744, 440, 'purple'), (745, 440, 'purple'), (746, 440, 'purple'), (747, 440, 'purple'), (748, 440, 'purple'), (749, 440, 'purple'), (750, 440, 'purple'), (751, 440, 'purple'), (752, 440, 'purple'), (753, 440, 'purple'), (754, 440, 'purple'), (772, 440, 'purple'), (756, 440, 'purple'), (757, 440, 'purple'), (758, 440, 'purple'), (759, 440, 'purple'), (760, 440, 'purple'), (761, 440, 'purple'), (762, 440, 'purple'), (763, 440, 'purple'), (764, 440, 'purple'), (765, 440, 'purple'), (766, 440, 'purple'), (767, 440, 'purple'), (768, 440, 'purple'), (769, 440, 'purple'), (770, 440, 'purple'), (771, 440, 'purple'), (778, 440, 'purple'), (773, 440, 'purple'), (774, 440, 'purple'), (775, 440, 'purple'), (776, 440, 'purple'), (777, 440, 'purple'), (782, 440, 'purple'), (779, 440, 'purple'), (780, 440, 'purple'), (781, 440, 'purple'), (784, 440, 'purple'), (783, 440, 'purple'), (779, 410, 'purple'), (784, 410, 'purple'), (780, 410, 'purple'), (781, 410, 'purple'), (782, 410, 'purple'), (783, 410, 'purple'), (791, 410, 'purple'), (785, 410, 'purple'), (786, 410, 'purple'), (787, 410, 'purple'), (788, 410, 'purple'), (789, 410, 'purple'), (790, 410, 'purple'), (802, 410, 'purple'), (792, 410, 'purple'), (793, 410, 'purple'), (794, 410, 'purple'), (795, 410, 'purple'), (796, 410, 'purple'), (797, 410, 'purple'), (798, 410, 'purple'), (799, 410, 'purple'), (800, 410, 'purple'), (801, 410, 'purple'), (814, 410, 'purple'), (803, 410, 'purple'), (804, 410, 'purple'), (805, 410, 'purple'), (806, 410, 'purple'), (807, 410, 'purple'), (808, 410, 'purple'), (809, 410, 'purple'), (810, 410, 'purple'), (811, 410, 'purple'), (812, 410, 'purple'), (813, 410, 'purple'), (831, 410, 'purple'), (815, 410, 'purple'), (816, 410, 'purple'), (817, 410, 'purple'), (818, 410, 'purple'), (819, 410, 'purple'), (820, 410, 'purple'), (821, 410, 'purple'), (822, 410, 'purple'), (823, 410, 'purple'), (824, 410, 'purple'), (825, 410, 'purple'), (826, 410, 'purple'), (827, 410, 'purple'), (828, 410, 'purple'), (829, 410, 'purple'), (830, 410, 'purple'), (843, 410, 'purple'), (832, 410, 'purple'), (833, 410, 'purple'), (834, 410, 'purple'), (835, 410, 'purple'), (836, 410, 'purple'), (837, 410, 'purple'), (838, 410, 'purple'), (839, 410, 'purple'), (840, 410, 'purple'), (841, 410, 'purple'), (842, 410, 'purple'), (851, 410, 'purple'), (844, 410, 'purple'), (845, 410, 'purple'), (846, 410, 'purple'), (847, 410, 'purple'), (848, 410, 'purple'), (849, 410, 'purple'), (850, 410, 'purple'), (854, 410, 'purple'), (852, 410, 'purple'), (853, 410, 'purple'), (858, 410, 'purple'), (855, 410, 'purple'), (856, 410, 'purple'), (857, 410, 'purple'), (818, 351, 'purple'), (819, 351, 'purple'), (825, 351, 'purple'), (820, 351, 'purple'), (821, 351, 'purple'), (822, 351, 'purple'), (823, 351, 'purple'), (824, 351, 'purple'), (833, 351, 'purple'), (826, 351, 'purple'), (827, 351, 'purple'), (828, 351, 'purple'), (829, 351, 'purple'), (830, 351, 'purple'), (831, 351, 'purple'), (832, 351, 'purple'), (843, 351, 'purple'), (834, 351, 'purple'), (835, 351, 'purple'), (836, 351, 'purple'), (837, 351, 'purple'), (838, 351, 'purple'), (839, 351, 'purple'), (840, 351, 'purple'), (841, 351, 'purple'), (842, 351, 'purple'), (868, 351, 'purple'), (844, 351, 'purple'), (845, 351, 'purple'), (846, 351, 'purple'), (847, 351, 'purple'), (848, 351, 'purple'), (849, 351, 'purple'), (850, 351, 'purple'), (851, 351, 'purple'), (852, 351, 'purple'), (853, 351, 'purple'), (854, 351, 'purple'), (855, 351, 'purple'), (856, 351, 'purple'), (857, 351, 'purple'), (858, 351, 'purple'), (859, 351, 'purple'), (860, 351, 'purple'), (861, 351, 'purple'), (862, 351, 'purple'), (863, 351, 'purple'), (864, 351, 'purple'), (865, 351, 'purple'), (866, 351, 'purple'), (867, 351, 'purple'), (876, 351, 'purple'), (869, 351, 'purple'), (870, 351, 'purple'), (871, 351, 'purple'), (872, 351, 'purple'), (873, 351, 'purple'), (874, 351, 'purple'), (875, 351, 'purple'), (888, 351, 'purple'), (877, 351, 'purple'), (878, 351, 'purple'), (879, 351, 'purple'), (880, 351, 'purple'), (881, 351, 'purple'), (882, 351, 'purple'), (883, 351, 'purple'), (884, 351, 'purple'), (885, 351, 'purple'), (886, 351, 'purple'), (887, 351, 'purple'), (893, 351, 'purple'), (889, 351, 'purple'), (890, 351, 'purple'), (891, 351, 'purple'), (892, 351, 'purple'), (894, 351, 'purple'), (101, 86, 'brown'), (106, 86, 'brown'), (102, 86, 'brown'), (103, 86, 'brown'), (104, 86, 'brown'), (105, 86, 'brown'), (117, 86, 'brown'), (107, 86, 'brown'), (108, 86, 'brown'), (109, 86, 'brown'), (110, 86, 'brown'), (111, 86, 'brown'), (112, 86, 'brown'), (113, 86, 'brown'), (114, 86, 'brown'), (115, 86, 'brown'), (116, 86, 'brown'), (148, 86, 'brown'), (118, 86, 'brown'), (119, 86, 'brown'), (120, 86, 'brown'), (121, 86, 'brown'), (122, 86, 'brown'), (123, 86, 'brown'), (124, 86, 'brown'), (125, 86, 'brown'), (126, 86, 'brown'), (127, 86, 'brown'), (128, 86, 'brown'), (129, 86, 'brown'), (130, 86, 'brown'), (131, 86, 'brown'), (132, 86, 'brown'), (133, 86, 'brown'), (134, 86, 'brown'), (135, 86, 'brown'), (136, 86, 'brown'), (137, 86, 'brown'), (138, 86, 'brown'), (139, 86, 'brown'), (140, 86, 'brown'), (141, 86, 'brown'), (142, 86, 'brown'), (143, 86, 'brown'), (144, 86, 'brown'), (145, 86, 'brown'), (146, 86, 'brown'), (147, 86, 'brown'), (197, 86, 'brown'), (149, 86, 'brown'), (150, 86, 'brown'), (151, 86, 'brown'), (152, 86, 'brown'), (153, 86, 'brown'), (154, 86, 'brown'), (155, 86, 'brown'), (156, 86, 'brown'), (157, 86, 'brown'), (158, 86, 'brown'), (159, 86, 'brown'), (160, 86, 'brown'), (161, 86, 'brown'), (162, 86, 'brown'), (163, 86, 'brown'), (164, 86, 'brown'), (165, 86, 'brown'), (166, 86, 'brown'), (167, 86, 'brown'), (168, 86, 'brown'), (169, 86, 'brown'), (170, 86, 'brown'), (171, 86, 'brown'), (172, 86, 'brown'), (173, 86, 'brown'), (174, 86, 'brown'), (175, 86, 'brown'), (176, 86, 'brown'), (177, 86, 'brown'), (178, 86, 'brown'), (179, 86, 'brown'), (180, 86, 'brown'), (181, 86, 'brown'), (182, 86, 'brown'), (183, 86, 'brown'), (184, 86, 'brown'), (185, 86, 'brown'), (186, 86, 'brown'), (187, 86, 'brown'), (188, 86, 'brown'), (189, 86, 'brown'), (190, 86, 'brown'), (191, 86, 'brown'), (192, 86, 'brown'), (193, 86, 'brown'), (194, 86, 'brown'), (195, 86, 'brown'), (196, 86, 'brown'), (225, 86, 'brown'), (198, 86, 'brown'), (199, 86, 'brown'), (200, 86, 'brown'), (201, 86, 'brown'), (202, 86, 'brown'), (203, 86, 'brown'), (204, 86, 'brown'), (205, 86, 'brown'), (206, 86, 'brown'), (207, 86, 'brown'), (208, 86, 'brown'), (209, 86, 'brown'), (210, 86, 'brown'), (211, 86, 'brown'), (212, 86, 'brown'), (213, 86, 'brown'), (214, 86, 'brown'), (215, 86, 'brown'), (216, 86, 'brown'), (217, 86, 'brown'), (218, 86, 'brown'), (219, 86, 'brown'), (220, 86, 'brown'), (221, 86, 'brown'), (222, 86, 'brown'), (223, 86, 'brown'), (224, 86, 'brown'), (247, 86, 'brown'), (226, 86, 'brown'), (227, 86, 'brown'), (228, 86, 'brown'), (229, 86, 'brown'), (230, 86, 'brown'), (231, 86, 'brown'), (232, 86, 'brown'), (233, 86, 'brown'), (234, 86, 'brown'), (235, 86, 'brown'), (236, 86, 'brown'), (237, 86, 'brown'), (238, 86, 'brown'), (239, 86, 'brown'), (240, 86, 'brown'), (241, 86, 'brown'), (242, 86, 'brown'), (243, 86, 'brown'), (244, 86, 'brown'), (245, 86, 'brown'), (246, 86, 'brown'), (259, 86, 'brown'), (248, 86, 'brown'), (249, 86, 'brown'), (250, 86, 'brown'), (251, 86, 'brown'), (252, 86, 'brown'), (253, 86, 'brown'), (254, 86, 'brown'), (255, 86, 'brown'), (256, 86, 'brown'), (257, 86, 'brown'), (258, 86, 'brown'), (262, 86, 'brown'), (260, 86, 'brown'), (261, 86, 'brown'), (240, 119, 'brown'), (243, 119, 'brown'), (241, 119, 'brown'), (242, 119, 'brown'), (251, 119, 'brown'), (244, 119, 'brown'), (245, 119, 'brown'), (246, 119, 'brown'), (247, 119, 'brown'), (248, 119, 'brown'), (249, 119, 'brown'), (250, 119, 'brown'), (272, 119, 'brown'), (252, 119, 'brown'), (253, 119, 'brown'), (254, 119, 'brown'), (255, 119, 'brown'), (256, 119, 'brown'), (257, 119, 'brown'), (258, 119, 'brown'), (259, 119, 'brown'), (260, 119, 'brown'), (261, 119, 'brown'), (262, 119, 'brown'), (263, 119, 'brown'), (264, 119, 'brown'), (265, 119, 'brown'), (266, 119, 'brown'), (267, 119, 'brown'), (268, 119, 'brown'), (269, 119, 'brown'), (270, 119, 'brown'), (271, 119, 'brown'), (309, 119, 'brown'), (273, 119, 'brown'), (274, 119, 'brown'), (275, 119, 'brown'), (276, 119, 'brown'), (277, 119, 'brown'), (278, 119, 'brown'), (279, 119, 'brown'), (280, 119, 'brown'), (281, 119, 'brown'), (282, 119, 'brown'), (283, 119, 'brown'), (284, 119, 'brown'), (285, 119, 'brown'), (286, 119, 'brown'), (287, 119, 'brown'), (288, 119, 'brown'), (289, 119, 'brown'), (290, 119, 'brown'), (291, 119, 'brown'), (292, 119, 'brown'), (293, 119, 'brown'), (294, 119, 'brown'), (295, 119, 'brown'), (296, 119, 'brown'), (297, 119, 'brown'), (298, 119, 'brown'), (299, 119, 'brown'), (300, 119, 'brown'), (301, 119, 'brown'), (302, 119, 'brown'), (303, 119, 'brown'), (304, 119, 'brown'), (305, 119, 'brown'), (306, 119, 'brown'), (307, 119, 'brown'), (308, 119, 'brown'), (346, 119, 'brown'), (310, 119, 'brown'), (311, 119, 'brown'), (312, 119, 'brown'), (313, 119, 'brown'), (314, 119, 'brown'), (315, 119, 'brown'), (316, 119, 'brown'), (317, 119, 'brown'), (318, 119, 'brown'), (319, 119, 'brown'), (320, 119, 'brown'), (321, 119, 'brown'), (322, 119, 'brown'), (323, 119, 'brown'), (324, 119, 'brown'), (325, 119, 'brown'), (326, 119, 'brown'), (327, 119, 'brown'), (328, 119, 'brown'), (329, 119, 'brown'), (330, 119, 'brown'), (331, 119, 'brown'), (332, 119, 'brown'), (333, 119, 'brown'), (334, 119, 'brown'), (335, 119, 'brown'), (336, 119, 'brown'), (337, 119, 'brown'), (338, 119, 'brown'), (339, 119, 'brown'), (340, 119, 'brown'), (341, 119, 'brown'), (342, 119, 'brown'), (343, 119, 'brown'), (344, 119, 'brown'), (345, 119, 'brown'), (364, 119, 'brown'), (347, 119, 'brown'), (348, 119, 'brown'), (349, 119, 'brown'), (350, 119, 'brown'), (351, 119, 'brown'), (352, 119, 'brown'), (353, 119, 'brown'), (354, 119, 'brown'), (355, 119, 'brown'), (356, 119, 'brown'), (357, 119, 'brown'), (358, 119, 'brown'), (359, 119, 'brown'), (360, 119, 'brown'), (361, 119, 'brown'), (362, 119, 'brown'), (363, 119, 'brown'), (374, 119, 'brown'), (365, 119, 'brown'), (366, 119, 'brown'), (367, 119, 'brown'), (368, 119, 'brown'), (369, 119, 'brown'), (370, 119, 'brown'), (371, 119, 'brown'), (372, 119, 'brown'), (373, 119, 'brown'), (379, 119, 'brown'), (375, 119, 'brown'), (376, 119, 'brown'), (377, 119, 'brown'), (378, 119, 'brown'), (355, 161, 'brown'), (358, 161, 'brown'), (356, 161, 'brown'), (357, 161, 'brown'), (367, 161, 'brown'), (359, 161, 'brown'), (360, 161, 'brown'), (361, 161, 'brown'), (362, 161, 'brown'), (363, 161, 'brown'), (364, 161, 'brown'), (365, 161, 'brown'), (366, 161, 'brown'), (391, 161, 'brown'), (368, 161, 'brown'), (369, 161, 'brown'), (370, 161, 'brown'), (371, 161, 'brown'), (372, 161, 'brown'), (373, 161, 'brown'), (374, 161, 'brown'), (375, 161, 'brown'), (376, 161, 'brown'), (377, 161, 'brown'), (378, 161, 'brown'), (379, 161, 'brown'), (380, 161, 'brown'), (381, 161, 'brown'), (382, 161, 'brown'), (383, 161, 'brown'), (384, 161, 'brown'), (385, 161, 'brown'), (386, 161, 'brown'), (387, 161, 'brown'), (388, 161, 'brown'), (389, 161, 'brown'), (390, 161, 'brown'), (414, 161, 'brown'), (392, 161, 'brown'), (393, 161, 'brown'), (394, 161, 'brown'), (395, 161, 'brown'), (396, 161, 'brown'), (397, 161, 'brown'), (398, 161, 'brown'), (399, 161, 'brown'), (400, 161, 'brown'), (401, 161, 'brown'), (402, 161, 'brown'), (403, 161, 'brown'), (404, 161, 'brown'), (405, 161, 'brown'), (406, 161, 'brown'), (407, 161, 'brown'), (408, 161, 'brown'), (409, 161, 'brown'), (410, 161, 'brown'), (411, 161, 'brown'), (412, 161, 'brown'), (413, 161, 'brown'), (474, 161, 'brown'), (415, 161, 'brown'), (416, 161, 'brown'), (417, 161, 'brown'), (418, 161, 'brown'), (419, 161, 'brown'), (420, 161, 'brown'), (421, 161, 'brown'), (422, 161, 'brown'), (423, 161, 'brown'), (424, 161, 'brown'), (425, 161, 'brown'), (426, 161, 'brown'), (427, 161, 'brown'), (428, 161, 'brown'), (429, 161, 'brown'), (430, 161, 'brown'), (431, 161, 'brown'), (432, 161, 'brown'), (433, 161, 'brown'), (434, 161, 'brown'), (435, 161, 'brown'), (436, 161, 'brown'), (437, 161, 'brown'), (438, 161, 'brown'), (439, 161, 'brown'), (440, 161, 'brown'), (441, 161, 'brown'), (442, 161, 'brown'), (443, 161, 'brown'), (444, 161, 'brown'), (445, 161, 'brown'), (446, 161, 'brown'), (447, 161, 'brown'), (448, 161, 'brown'), (449, 161, 'brown'), (450, 161, 'brown'), (451, 161, 'brown'), (452, 161, 'brown'), (453, 161, 'brown'), (454, 161, 'brown'), (455, 161, 'brown'), (456, 161, 'brown'), (457, 161, 'brown'), (458, 161, 'brown'), (459, 161, 'brown'), (460, 161, 'brown'), (461, 161, 'brown'), (462, 161, 'brown'), (463, 161, 'brown'), (464, 161, 'brown'), (465, 161, 'brown'), (466, 161, 'brown'), (467, 161, 'brown'), (468, 161, 'brown'), (469, 161, 'brown'), (470, 161, 'brown'), (471, 161, 'brown'), (472, 161, 'brown'), (473, 161, 'brown'), (515, 161, 'brown'), (475, 161, 'brown'), (476, 161, 'brown'), (477, 161, 'brown'), (478, 161, 'brown'), (479, 161, 'brown'), (480, 161, 'brown'), (481, 161, 'brown'), (482, 161, 'brown'), (483, 161, 'brown'), (484, 161, 'brown'), (485, 161, 'brown'), (486, 161, 'brown'), (487, 161, 'brown'), (488, 161, 'brown'), (489, 161, 'brown'), (490, 161, 'brown'), (491, 161, 'brown'), (492, 161, 'brown'), (493, 161, 'brown'), (494, 161, 'brown'), (495, 161, 'brown'), (496, 161, 'brown'), (497, 161, 'brown'), (498, 161, 'brown'), (499, 161, 'brown'), (500, 161, 'brown'), (501, 161, 'brown'), (502, 161, 'brown'), (503, 161, 'brown'), (504, 161, 'brown'), (505, 161, 'brown'), (506, 161, 'brown'), (507, 161, 'brown'), (508, 161, 'brown'), (509, 161, 'brown'), (510, 161, 'brown'), (511, 161, 'brown'), (512, 161, 'brown'), (513, 161, 'brown'), (514, 161, 'brown'), (559, 161, 'brown'), (516, 161, 'brown'), (517, 161, 'brown'), (518, 161, 'brown'), (519, 161, 'brown'), (520, 161, 'brown'), (521, 161, 'brown'), (522, 161, 'brown'), (523, 161, 'brown'), (524, 161, 'brown'), (525, 161, 'brown'), (526, 161, 'brown'), (527, 161, 'brown'), (528, 161, 'brown'), (529, 161, 'brown'), (530, 161, 'brown'), (531, 161, 'brown'), (532, 161, 'brown'), (533, 161, 'brown'), (534, 161, 'brown'), (535, 161, 'brown'), (536, 161, 'brown'), (537, 161, 'brown'), (538, 161, 'brown'), (539, 161, 'brown'), (540, 161, 'brown'), (541, 161, 'brown'), (542, 161, 'brown'), (543, 161, 'brown'), (544, 161, 'brown'), (545, 161, 'brown'), (546, 161, 'brown'), (547, 161, 'brown'), (548, 161, 'brown'), (549, 161, 'brown'), (550, 161, 'brown'), (551, 161, 'brown'), (552, 161, 'brown'), (553, 161, 'brown'), (554, 161, 'brown'), (555, 161, 'brown'), (556, 161, 'brown'), (557, 161, 'brown'), (558, 161, 'brown'), (566, 161, 'brown'), (560, 161, 'brown'), (561, 161, 'brown'), (562, 161, 'brown'), (563, 161, 'brown'), (564, 161, 'brown'), (565, 161, 'brown'), (579, 161, 'brown'), (567, 161, 'brown'), (568, 161, 'brown'), (569, 161, 'brown'), (570, 161, 'brown'), (571, 161, 'brown'), (572, 161, 'brown'), (573, 161, 'brown'), (574, 161, 'brown'), (575, 161, 'brown'), (576, 161, 'brown'), (577, 161, 'brown'), (578, 161, 'brown'), (582, 161, 'brown'), (580, 161, 'brown'), (581, 161, 'brown'), (56, 445, 'orange'), (56, 444, 'orange'), (56, 443, 'orange'), (56, 442, 'orange'), (56, 441, 'orange'), (56, 440, 'orange'), (57, 437, 'orange'), (59, 434, 'orange'), (60, 433, 'orange'), (62, 429, 'orange'), (64, 425, 'orange'), (65, 422, 'orange'), (67, 420, 'orange'), (68, 418, 'orange'), (69, 416, 'orange'), (69, 414, 'orange'), (69, 415, 'orange'), (70, 414, 'orange'), (70, 413, 'orange'), (70, 412, 'orange'), (71, 412, 'orange'), (71, 411, 'orange'), (71, 410, 'orange'), (72, 410, 'orange'), (72, 409, 'orange'), (73, 409, 'orange'), (73, 408, 'orange'), (74, 407, 'orange'), (74, 406, 'orange'), (75, 406, 'orange'), (75, 405, 'orange'), (76, 404, 'orange'), (76, 403, 'orange'), (77, 402, 'orange'), (77, 401, 'orange'), (78, 401, 'orange'), (78, 400, 'orange'), (79, 400, 'orange'), (79, 401, 'orange'), (80, 402, 'orange'), (81, 403, 'orange'), (81, 404, 'orange'), (82, 404, 'orange'), (82, 405, 'orange'), (83, 406, 'orange'), (85, 408, 'orange'), (90, 412, 'orange'), (96, 417, 'orange'), (105, 424, 'orange'), (114, 434, 'orange'), (121, 440, 'orange'), (127, 445, 'orange'), (130, 448, 'orange'), (132, 450, 'orange'), (132, 451, 'orange'), (133, 451, 'orange'), (133, 450, 'orange'), (133, 449, 'orange'), (133, 448, 'orange'), (133, 447, 'orange'), (133, 446, 'orange'), (133, 442, 'orange'), (133, 445, 'orange'), (133, 444, 'orange'), (133, 443, 'orange'), (134, 439, 'orange'), (136, 434, 'orange'), (138, 430, 'orange'), (142, 425, 'orange'), (146, 419, 'orange'), (150, 415, 'orange'), (152, 411, 'orange'), (154, 409, 'orange'), (155, 407, 'orange'), (156, 406, 'orange'), (157, 406, 'orange'), (157, 405, 'orange'), (158, 404, 'orange'), (159, 403, 'orange'), (159, 402, 'orange'), (160, 402, 'orange'), (160, 401, 'orange'), (161, 401, 'orange'), (161, 400, 'orange'), (161, 399, 'orange'), (162, 399, 'orange'), (162, 398, 'orange'), (163, 398, 'orange'), (163, 399, 'orange'), (162, 400, 'orange'), (26, 224, 'orange'), (26, 223, 'orange'), (26, 221, 'orange'), (26, 222, 'orange'), (27, 219, 'orange'), (28, 217, 'orange'), (30, 209, 'orange'), (33, 201, 'orange'), (34, 194, 'orange'), (37, 186, 'orange'), (38, 181, 'orange'), (40, 177, 'orange'), (40, 176, 'orange'), (41, 175, 'orange'), (41, 174, 'orange'), (42, 175, 'orange'), (42, 176, 'orange'), (43, 178, 'orange'), (44, 181, 'orange'), (45, 185, 'orange'), (49, 189, 'orange'), (54, 196, 'orange'), (57, 201, 'orange'), (63, 209, 'orange'), (66, 214, 'orange'), (70, 220, 'orange'), (73, 224, 'orange'), (75, 227, 'orange'), (76, 228, 'orange'), (76, 229, 'orange'), (77, 230, 'orange'), (78, 230, 'orange'), (78, 231, 'orange'), (79, 231, 'orange'), (80, 231, 'orange'), (82, 229, 'orange'), (84, 228, 'orange'), (88, 226, 'orange'), (92, 223, 'orange'), (107, 213, 'orange'), (134, 194, 'orange'), (151, 182, 'orange'), (161, 175, 'orange'), (165, 172, 'orange'), (182, 160, 'orange'), (185, 158, 'orange'), (188, 156, 'orange'), (189, 156, 'orange'), (188, 156, 'orange'), (186, 157, 'orange'), (947, 185, 'orange'), (949, 187, 'orange'), (957, 193, 'orange'), (964, 201, 'orange'), (976, 213, 'orange'), (1000, 237, 'orange'), (1016, 253, 'orange'), (1041, 273, 'orange'), (1050, 281, 'orange'), (1055, 283, 'orange'), (1056, 283, 'orange'), (1058, 283, 'orange'), (1057, 283, 'orange'), (1059, 283, 'orange'), (1059, 282, 'orange'), (1060, 280, 'orange'), (1062, 276, 'orange'), (1066, 272, 'orange'), (1076, 264, 'orange'), (1083, 258, 'orange'), (1092, 251, 'orange'), (1108, 241, 'orange'), (1117, 234, 'orange'), (1125, 229, 'orange'), (1129, 227, 'orange'), (1130, 227, 'orange'), (1131, 227, 'orange'), (1131, 230, 'orange'), (1131, 229, 'orange'), (1131, 228, 'orange'), (1134, 236, 'orange'), (1138, 244, 'orange'), (1141, 250, 'orange'), (1151, 266, 'orange'), (1157, 275, 'orange'), (1162, 284, 'orange'), (1166, 289, 'orange'), (1168, 292, 'orange'), (1168, 293, 'orange'), (1124, 400, 'orange'), (1119, 400, 'orange'), (1120, 400, 'orange'), (1121, 400, 'orange'), (1122, 400, 'orange'), (1123, 400, 'orange'), (1110, 398, 'orange'), (1102, 393, 'orange'), (1071, 379, 'orange'), (1029, 357, 'orange'), (985, 331, 'orange'), (943, 304, 'orange'), (921, 288, 'orange'), (892, 266, 'orange'), (884, 259, 'orange'), (878, 253, 'orange'), (869, 246, 'orange'), (866, 243, 'orange'), (863, 240, 'orange'), (862, 240, 'orange'), (861, 240, 'orange')]
    
    Tuple=[(25, 287, 'black'), (26, 287, 'black'), (29, 287, 'black'), (27, 287, 'black'), (33, 287, 'black'), (30, 287, 'black'), (32, 287, 'black'), (37, 287, 'black'), (34, 287, 'black'), (36, 287, 'black'), (61, 287, 'black'), (38, 287, 'black'), (40, 287, 'black'), (42, 287, 'black'), (44, 287, 'black'), (46, 287, 'black'), (48, 287, 'black'), (50, 287, 'black'), (52, 287, 'black'), (54, 287, 'black'), (56, 287, 'black'), (58, 287, 'black'), (60, 287, 'black'), (68, 287, 'black'), (62, 287, 'black'), (64, 287, 'black'), (66, 287, 'black'), (91, 287, 'black'), (69, 287, 'black'), (71, 287, 'black'), (73, 287, 'black'), (75, 287, 'black'), (77, 287, 'black'), (79, 287, 'black'), (81, 287, 'black'), (83, 287, 'black'), (85, 287, 'black'), (87, 287, 'black'), (89, 287, 'black'), (118, 287, 'black'), (92, 287, 'black'), (94, 287, 'black'), (96, 287, 'black'), (98, 287, 'black'), (100, 287, 'black'), (102, 287, 'black'), (104, 287, 'black'), (106, 287, 'black'), (108, 287, 'black'), (110, 287, 'black'), (112, 287, 'black'), (114, 287, 'black'), (116, 287, 'black'), (143, 288, 'black'), (163, 289, 'black'), (179, 289, 'black'), (164, 289, 'black'), (166, 289, 'black'), (168, 289, 'black'), (170, 289, 'black'), (172, 289, 'black'), (174, 289, 'black'), (176, 289, 'black'), (178, 289, 'black'), (189, 289, 'black'), (180, 289, 'black'), (182, 289, 'black'), (184, 289, 'black'), (186, 289, 'black'), (188, 289, 'black'), (199, 289, 'black'), (190, 289, 'black'), (192, 289, 'black'), (194, 289, 'black'), (196, 289, 'black'), (198, 289, 'black'), (204, 289, 'black'), (200, 289, 'black'), (202, 289, 'black'), (208, 289, 'black'), (205, 289, 'black'), (207, 289, 'black'), (209, 289, 'black'), (210, 289, 'black'), (211, 289, 'black'), (210, 289, 'black'), (250, 166, 'black'), (251, 167, 'black'), (252, 169, 'black'), (254, 171, 'black'), (257, 174, 'black'), (259, 178, 'black'), (264, 184, 'black'), (275, 198, 'black'), (295, 224, 'black'), (316, 255, 'black'), (334, 281, 'black'), (349, 302, 'black'), (367, 328, 'black'), (382, 351, 'black'), (390, 361, 'black'), (396, 371, 'black'), (401, 378, 'black'), (405, 383, 'black'), (411, 390, 'black'), (414, 395, 'black'), (418, 400, 'black'), (422, 404, 'black'), (422, 405, 'black'), (424, 406, 'black'), (424, 407, 'black'), (447, 254, 'purple'), (448, 254, 'purple'), (449, 254, 'purple'), (450, 254, 'purple'), (451, 254, 'purple'), (453, 254, 'purple'), (452, 254, 'purple'), (454, 254, 'purple'), (456, 254, 'purple'), (455, 254, 'purple'), (458, 254, 'purple'), (457, 254, 'purple'), (460, 254, 'purple'), (459, 254, 'purple'), (462, 254, 'purple'), (461, 254, 'purple'), (465, 254, 'purple'), (463, 254, 'purple'), (467, 254, 'purple'), (466, 254, 'purple'), (469, 254, 'purple'), (468, 254, 'purple'), (471, 254, 'purple'), (470, 254, 'purple'), (472, 254, 'purple'), (473, 254, 'purple'), (475, 254, 'purple'), (474, 254, 'purple'), (476, 254, 'purple'), (478, 254, 'purple'), (477, 254, 'purple'), (480, 254, 'purple'), (479, 254, 'purple'), (482, 254, 'purple'), (481, 254, 'purple'), (484, 254, 'purple'), (483, 254, 'purple'), (486, 254, 'purple'), (485, 254, 'purple'), (488, 254, 'purple'), (487, 254, 'purple'), (491, 254, 'purple'), (489, 254, 'purple'), (493, 254, 'purple'), (492, 254, 'purple'), (495, 254, 'purple'), (494, 254, 'purple'), (497, 254, 'purple'), (496, 254, 'purple'), (500, 254, 'purple'), (498, 254, 'purple'), (503, 254, 'purple'), (501, 254, 'purple'), (506, 254, 'purple'), (504, 254, 'purple'), (509, 255, 'purple'), (512, 255, 'purple'), (510, 255, 'purple'), (514, 255, 'purple'), (513, 255, 'purple'), (516, 255, 'purple'), (515, 255, 'purple'), (517, 255, 'purple'), (519, 255, 'purple'), (518, 255, 'purple'), (520, 255, 'purple'), (523, 255, 'purple'), (521, 255, 'purple'), (524, 255, 'purple'), (527, 255, 'purple'), (525, 255, 'purple'), (528, 255, 'purple'), (530, 255, 'purple'), (529, 255, 'purple'), (532, 255, 'purple'), (531, 255, 'purple'), (535, 256, 'purple'), (537, 256, 'purple'), (536, 256, 'purple'), (540, 256, 'purple'), (538, 256, 'purple'), (542, 256, 'purple'), (541, 256, 'purple'), (544, 256, 'purple'), (543, 256, 'purple'), (545, 256, 'purple'), (546, 256, 'purple'), (547, 256, 'purple'), (548, 256, 'purple'), (549, 256, 'purple'), (550, 256, 'purple'), (551, 256, 'purple'), (553, 256, 'purple'), (552, 256, 'purple'), (557, 256, 'purple'), (554, 256, 'purple'), (556, 256, 'purple'), (561, 256, 'purple'), (558, 256, 'purple'), (560, 256, 'purple'), (564, 256, 'purple'), (562, 256, 'purple'), (568, 256, 'purple'), (565, 256, 'purple'), (567, 256, 'purple'), (570, 256, 'purple'), (569, 256, 'purple'), (572, 256, 'purple'), (571, 256, 'purple'), (573, 256, 'purple'), (574, 256, 'purple'), (575, 256, 'purple'), (577, 256, 'purple'), (576, 256, 'purple'), (579, 256, 'purple'), (578, 256, 'purple'), (581, 256, 'purple'), (580, 256, 'purple'), (583, 256, 'purple'), (582, 256, 'purple'), (584, 256, 'purple'), (585, 256, 'purple'), (586, 256, 'purple'), (587, 256, 'purple'), (588, 256, 'purple'), (589, 256, 'purple'), (590, 256, 'purple'), (592, 256, 'purple'), (591, 256, 'purple'), (594, 256, 'purple'), (593, 256, 'purple'), (595, 256, 'purple'), (596, 256, 'purple'), (598, 256, 'purple'), (597, 256, 'purple'), (599, 256, 'purple'), (600, 256, 'purple'), (601, 256, 'purple'), (602, 256, 'purple'), (603, 256, 'purple'), (604, 256, 'purple'), (605, 256, 'purple'), (606, 256, 'purple'), (607, 256, 'purple'), (608, 256, 'purple'), (609, 256, 'purple'), (635, 171, 'purple'), (636, 171, 'purple'), (637, 171, 'purple'), (637, 172, 'purple'), (641, 175, 'purple'), (644, 178, 'purple'), (649, 180, 'purple'), (651, 183, 'purple'), (653, 184, 'purple'), (654, 185, 'purple'), (656, 187, 'purple'), (658, 190, 'purple'), (659, 192, 'purple'), (661, 194, 'purple'), (666, 201, 'purple'), (672, 207, 'purple'), (678, 215, 'purple'), (684, 222, 'purple'), (694, 231, 'purple'), (703, 240, 'purple'), (708, 247, 'purple'), (714, 253, 'purple'), (720, 258, 'purple'), (725, 264, 'purple'), (729, 268, 'purple'), (735, 273, 'purple'), (742, 280, 'purple'), (746, 285, 'purple'), (752, 290, 'purple'), (757, 297, 'purple'), (762, 302, 'purple'), (766, 307, 'purple'), (770, 313, 'purple'), (774, 317, 'purple'), (778, 322, 'purple'), (786, 332, 'purple'), (790, 336, 'purple'), (796, 342, 'purple'), (800, 348, 'purple'), (805, 353, 'purple'), (808, 356, 'purple'), (810, 358, 'purple'), (811, 360, 'purple'), (812, 360, 'purple'), (813, 361, 'purple'), (813, 362, 'purple'), (814, 362, 'purple'), (814, 363, 'purple'), (815, 363, 'purple'), (816, 365, 'purple'), (818, 367, 'purple'), (818, 368, 'purple'), (819, 369, 'purple'), (820, 369, 'purple')]
    '''
    #Tuple=[(131, 371, 'black'), (131, 370, 'black'), (131, 369, 'black'), (131, 368, 'black'), (131, 365, 'black'), (131, 367, 'black'), (131, 366, 'black'), (132, 363, 'black'), (132, 360, 'black'), (132, 362, 'black'), (132, 361, 'black'), (133, 359, 'black'), (133, 357, 'black'), (133, 358, 'black'), (133, 356, 'black'), (134, 355, 'black'), (134, 354, 'black'), (134, 352, 'black'), (134, 353, 'black'), (134, 351, 'black'), (135, 349, 'black'), (135, 348, 'black'), (136, 346, 'black'), (136, 344, 'black'), (136, 345, 'black'), (137, 343, 'black'), (137, 341, 'black'), (137, 342, 'black'), (137, 340, 'black'), (138, 339, 'black'), (138, 338, 'black'), (138, 337, 'black'), (138, 336, 'black'), (139, 336, 'black'), (140, 335, 'black'), (140, 334, 'black'), (141, 334, 'black'), (141, 333, 'black'), (141, 332, 'black'), (142, 330, 'black'), (143, 329, 'black'), (144, 328, 'black'), (144, 327, 'black'), (145, 327, 'black'), (145, 326, 'black'), (146, 326, 'black'), (146, 325, 'black'), (147, 324, 'black'), (147, 323, 'black'), (148, 322, 'black'), (148, 321, 'black'), (149, 319, 'black'), (151, 317, 'black'), (151, 316, 'black'), (152, 314, 'black'), (153, 313, 'black'), (154, 312, 'black'), (154, 311, 'black'), (155, 310, 'black'), (155, 309, 'black'), (156, 309, 'black'), (156, 308, 'black'), (157, 308, 'black'), (158, 307, 'black'), (159, 305, 'black'), (160, 304, 'black'), (161, 302, 'black'), (162, 301, 'black'), (163, 300, 'black'), (164, 299, 'black'), (165, 298, 'black'), (166, 298, 'black'), (166, 297, 'black'), (167, 297, 'black'), (168, 296, 'black'), (169, 295, 'black'), (170, 294, 'black'), (172, 293, 'black'), (173, 291, 'black'), (174, 291, 'black'), (175, 290, 'black'), (176, 289, 'black'), (177, 289, 'black'), (177, 288, 'black'), (178, 288, 'black'), (178, 287, 'black'), (179, 287, 'black'), (180, 287, 'black'), (180, 286, 'black'), (181, 286, 'black'), (182, 285, 'black'), (183, 284, 'black'), (184, 284, 'black'), (187, 282, 'black'), (188, 281, 'black'), (190, 280, 'black'), (192, 280, 'black'), (191, 280, 'black'), (193, 279, 'black'), (194, 279, 'black'), (195, 278, 'black'), (196, 277, 'black'), (197, 277, 'black'), (198, 276, 'black'), (199, 276, 'black'), (200, 275, 'black'), (201, 275, 'black'), (202, 274, 'black'), (204, 274, 'black'), (203, 274, 'black'), (205, 273, 'black'), (206, 273, 'black'), (207, 273, 'black'), (208, 272, 'black'), (209, 272, 'black'), (210, 272, 'black'), (211, 272, 'black'), (212, 272, 'black'), (212, 271, 'black'), (213, 271, 'black'), (214, 271, 'black'), (215, 271, 'black'), (216, 270, 'black'), (217, 270, 'black'), (218, 270, 'black'), (221, 269, 'black'), (223, 268, 'black'), (225, 268, 'black'), (224, 268, 'black'), (226, 267, 'black'), (227, 267, 'black'), (228, 267, 'black'), (230, 266, 'black'), (231, 266, 'black'), (232, 266, 'black'), (233, 266, 'black'), (234, 265, 'black'), (235, 265, 'black'), (236, 265, 'black'), (238, 264, 'black'), (240, 264, 'black'), (239, 264, 'black'), (243, 263, 'black'), (246, 262, 'black'), (248, 261, 'black'), (250, 261, 'black'), (249, 261, 'black'), (251, 260, 'black'), (252, 260, 'black'), (253, 260, 'black'), (255, 260, 'black'), (254, 260, 'black'), (256, 259, 'black'), (259, 259, 'black'), (257, 259, 'black'), (258, 259, 'black'), (265, 258, 'black'), (269, 257, 'black'), (273, 256, 'black'), (276, 256, 'black'), (274, 256, 'black'), (275, 256, 'black'), (278, 256, 'black'), (277, 256, 'black'), (279, 255, 'black'), (280, 255, 'black'), (281, 255, 'black'), (282, 255, 'black'), (283, 255, 'black'), (285, 255, 'black'), (284, 255, 'black'), (289, 255, 'black'), (286, 255, 'black'), (287, 255, 'black'), (288, 255, 'black'), (293, 255, 'black'), (290, 255, 'black'), (291, 255, 'black'), (292, 255, 'black'), (298, 255, 'black'), (294, 255, 'black'), (295, 255, 'black'), (296, 255, 'black'), (297, 255, 'black'), (302, 255, 'black'), (299, 255, 'black'), (300, 255, 'black'), (301, 255, 'black'), (305, 256, 'black'), (309, 257, 'black'), (312, 257, 'black'), (310, 257, 'black'), (311, 257, 'black'), (316, 258, 'black'), (318, 259, 'black'), (321, 259, 'black'), (319, 259, 'black'), (320, 259, 'black'), (324, 260, 'black'), (326, 261, 'black'), (327, 261, 'black'), (330, 263, 'black'), (333, 264, 'black'), (336, 265, 'black'), (338, 266, 'black'), (341, 268, 'black'), (344, 270, 'black'), (348, 272, 'black'), (350, 273, 'black'), (353, 276, 'black'), (356, 278, 'black'), (359, 280, 'black'), (362, 283, 'black'), (366, 286, 'black'), (369, 289, 'black'), (373, 292, 'black'), (377, 296, 'black'), (383, 301, 'black'), (386, 304, 'black'), (389, 307, 'black'), (392, 310, 'black'), (394, 313, 'black'), (396, 315, 'black'), (398, 317, 'black'), (400, 319, 'black'), (402, 321, 'black'), (405, 323, 'black'), (407, 325, 'black'), (409, 327, 'black'), (411, 329, 'black'), (413, 330, 'black'), (415, 332, 'black'), (417, 334, 'black'), (419, 336, 'black'), (420, 337, 'black'), (423, 338, 'black'), (425, 340, 'black'), (427, 341, 'black'), (430, 342, 'black'), (433, 343, 'black'), (436, 344, 'black'), (438, 345, 'black'), (441, 346, 'black'), (443, 346, 'black'), (442, 346, 'black'), (445, 347, 'black'), (447, 348, 'black'), (449, 348, 'black'), (448, 348, 'black'), (451, 348, 'black'), (450, 348, 'black'), (454, 348, 'black'), (452, 348, 'black'), (453, 348, 'black'), (458, 348, 'black'), (455, 348, 'black'), (456, 348, 'black'), (457, 348, 'black'), (461, 348, 'black'), (459, 348, 'black'), (460, 348, 'black'), (467, 348, 'black'), (462, 348, 'black'), (463, 348, 'black'), (464, 348, 'black'), (465, 348, 'black'), (466, 348, 'black'), (471, 348, 'black'), (468, 348, 'black'), (469, 348, 'black'), (470, 348, 'black'), (475, 347, 'black'), (479, 346, 'black'), (482, 344, 'black'), (486, 343, 'black'), (488, 341, 'black'), (491, 339, 'black'), (493, 338, 'black'), (496, 336, 'black'), (498, 334, 'black'), (500, 332, 'black'), (501, 330, 'black'), (502, 329, 'black'), (503, 328, 'black'), (504, 327, 'black'), (506, 325, 'black'), (507, 323, 'black'), (508, 322, 'black'), (509, 321, 'black'), (510, 320, 'black'), (511, 318, 'black'), (512, 317, 'black'), (513, 316, 'black'), (514, 315, 'black'), (515, 313, 'black'), (516, 312, 'black'), (517, 310, 'black'), (519, 308, 'black'), (521, 307, 'black'), (523, 305, 'black'), (525, 303, 'black'), (528, 300, 'black'), (531, 298, 'black'), (533, 296, 'black'), (535, 294, 'black'), (537, 293, 'black'), (539, 291, 'black'), (540, 290, 'black'), (541, 289, 'black'), (541, 288, 'black'), (542, 287, 'black'), (543, 286, 'black'), (543, 285, 'black'), (544, 285, 'black'), (544, 284, 'black'), (544, 283, 'black'), (545, 283, 'black'), (545, 282, 'black'), (545, 281, 'black'), (546, 280, 'black'), (546, 279, 'black'), (547, 278, 'black'), (547, 277, 'black'), (547, 276, 'black'), (100, 232, 'orange'), (101, 232, 'orange'), (102, 232, 'orange'), (102, 231, 'orange'), (103, 231, 'orange'), (104, 229, 'orange'), (105, 229, 'orange'), (106, 229, 'orange'), (107, 227, 'orange'), (108, 227, 'orange'), (110, 225, 'orange'), (111, 224, 'orange'), (113, 223, 'orange'), (114, 223, 'orange'), (115, 222, 'orange'), (116, 221, 'orange'), (118, 220, 'orange'), (119, 220, 'orange'), (120, 219, 'orange'), (121, 218, 'orange'), (122, 218, 'orange'), (123, 217, 'orange'), (124, 216, 'orange'), (125, 216, 'orange'), (126, 215, 'orange'), (127, 215, 'orange'), (128, 214, 'orange'), (129, 213, 'orange'), (130, 213, 'orange'), (131, 212, 'orange'), (132, 212, 'orange'), (133, 211, 'orange'), (134, 211, 'orange'), (135, 210, 'orange'), (136, 210, 'orange'), (137, 209, 'orange'), (138, 209, 'orange'), (139, 209, 'orange'), (140, 208, 'orange'), (141, 208, 'orange'), (142, 208, 'orange'), (143, 207, 'orange'), (144, 207, 'orange'), (147, 206, 'orange'), (148, 206, 'orange'), (151, 205, 'orange'), (154, 204, 'orange'), (157, 204, 'orange'), (155, 204, 'orange'), (156, 204, 'orange'), (159, 203, 'orange'), (162, 203, 'orange'), (160, 203, 'orange'), (161, 203, 'orange'), (165, 202, 'orange'), (168, 202, 'orange'), (166, 202, 'orange'), (167, 202, 'orange'), (170, 201, 'orange'), (172, 201, 'orange'), (171, 201, 'orange'), (174, 201, 'orange'), (173, 201, 'orange'), (175, 200, 'orange'), (177, 200, 'orange'), (176, 200, 'orange'), (178, 200, 'orange'), (180, 200, 'orange'), (179, 200, 'orange'), (182, 200, 'orange'), (181, 200, 'orange'), (184, 199, 'orange'), (186, 199, 'orange'), (185, 199, 'orange'), (188, 199, 'orange'), (187, 199, 'orange'), (189, 199, 'orange'), (191, 199, 'orange'), (190, 199, 'orange'), (193, 199, 'orange'), (192, 199, 'orange'), (194, 199, 'orange'), (196, 199, 'orange'), (195, 199, 'orange'), (198, 199, 'orange'), (197, 199, 'orange'), (201, 199, 'orange'), (199, 199, 'orange'), (200, 199, 'orange'), (203, 199, 'orange'), (202, 199, 'orange'), (206, 199, 'orange'), (204, 199, 'orange'), (205, 199, 'orange'), (208, 199, 'orange'), (207, 199, 'orange'), (210, 199, 'orange'), (209, 199, 'orange'), (212, 199, 'orange'), (211, 199, 'orange'), (214, 199, 'orange'), (213, 199, 'orange'), (215, 199, 'orange'), (218, 199, 'orange'), (216, 199, 'orange'), (217, 199, 'orange'), (220, 199, 'orange'), (219, 199, 'orange'), (221, 199, 'orange'), (224, 199, 'orange'), (222, 199, 'orange'), (223, 199, 'orange'), (226, 199, 'orange'), (225, 199, 'orange'), (228, 199, 'orange'), (227, 199, 'orange'), (231, 199, 'orange'), (229, 199, 'orange'), (230, 199, 'orange'), (234, 199, 'orange'), (232, 199, 'orange'), (233, 199, 'orange'), (237, 199, 'orange'), (235, 199, 'orange'), (236, 199, 'orange'), (239, 199, 'orange'), (238, 199, 'orange'), (242, 199, 'orange'), (240, 199, 'orange'), (241, 199, 'orange'), (244, 199, 'orange'), (243, 199, 'orange'), (246, 199, 'orange'), (245, 199, 'orange'), (248, 199, 'orange'), (247, 199, 'orange'), (250, 199, 'orange'), (249, 199, 'orange'), (251, 199, 'orange'), (253, 199, 'orange'), (252, 199, 'orange'), (254, 199, 'orange'), (255, 199, 'orange'), (256, 199, 'orange'), (257, 199, 'orange'), (258, 199, 'orange'), (259, 199, 'orange'), (260, 199, 'orange'), (261, 199, 'orange'), (263, 199, 'orange'), (262, 199, 'orange'), (265, 200, 'orange'), (266, 200, 'orange'), (268, 200, 'orange'), (267, 200, 'orange'), (269, 200, 'orange'), (270, 200, 'orange'), (272, 200, 'orange'), (271, 200, 'orange'), (273, 200, 'orange'), (274, 200, 'orange'), (276, 200, 'orange'), (275, 200, 'orange'), (277, 200, 'orange'), (279, 200, 'orange'), (278, 200, 'orange'), (280, 200, 'orange'), (282, 200, 'orange'), (281, 200, 'orange'), (283, 200, 'orange'), (285, 200, 'orange'), (284, 200, 'orange'), (286, 200, 'orange'), (287, 200, 'orange'), (288, 200, 'orange'), (289, 200, 'orange'), (290, 200, 'orange'), (291, 200, 'orange'), (292, 200, 'orange'), (293, 200, 'orange'), (294, 200, 'orange'), (295, 200, 'orange'), (296, 200, 'orange'), (297, 200, 'orange'), (298, 200, 'orange'), (299, 200, 'orange'), (300, 200, 'orange'), (301, 200, 'orange'), (303, 200, 'orange'), (302, 200, 'orange'), (304, 200, 'orange'), (306, 200, 'orange'), (305, 200, 'orange'), (307, 200, 'orange'), (308, 200, 'orange'), (309, 200, 'orange'), (310, 200, 'orange'), (311, 200, 'orange'), (312, 200, 'orange'), (313, 200, 'orange'), (314, 200, 'orange'), (315, 200, 'orange'), (316, 200, 'orange'), (317, 200, 'orange'), (318, 200, 'orange'), (319, 200, 'orange'), (321, 200, 'orange'), (320, 200, 'orange'), (323, 200, 'orange'), (322, 200, 'orange'), (324, 200, 'orange'), (325, 200, 'orange'), (326, 200, 'orange'), (326, 199, 'orange'), (327, 199, 'orange'), (328, 199, 'orange'), (329, 199, 'orange'), (330, 199, 'orange'), (331, 199, 'orange'), (334, 199, 'orange'), (332, 199, 'orange'), (333, 199, 'orange'), (337, 199, 'orange'), (335, 199, 'orange'), (336, 199, 'orange'), (339, 199, 'orange'), (338, 199, 'orange'), (341, 199, 'orange'), (340, 199, 'orange'), (342, 199, 'orange'), (344, 199, 'orange'), (343, 199, 'orange'), (345, 199, 'orange'), (347, 199, 'orange'), (346, 199, 'orange'), (348, 199, 'orange'), (350, 199, 'orange'), (349, 199, 'orange'), (351, 199, 'orange'), (352, 199, 'orange'), (354, 199, 'orange'), (353, 199, 'orange'), (356, 199, 'orange'), (355, 199, 'orange'), (357, 199, 'orange'), (359, 199, 'orange'), (358, 199, 'orange'), (360, 199, 'orange'), (362, 199, 'orange'), (361, 199, 'orange'), (363, 199, 'orange'), (364, 199, 'orange'), (365, 199, 'orange'), (366, 199, 'orange'), (367, 199, 'orange'), (368, 199, 'orange'), (369, 199, 'orange'), (370, 199, 'orange'), (371, 199, 'orange'), (373, 199, 'orange'), (372, 199, 'orange'), (374, 199, 'orange'), (376, 199, 'orange'), (375, 199, 'orange'), (377, 199, 'orange'), (379, 199, 'orange'), (378, 199, 'orange'), (380, 199, 'orange'), (381, 199, 'orange'), (384, 199, 'orange'), (382, 199, 'orange'), (383, 199, 'orange'), (386, 199, 'orange'), (385, 199, 'orange'), (388, 199, 'orange'), (387, 199, 'orange'), (389, 199, 'orange'), (390, 199, 'orange'), (391, 199, 'orange'), (392, 199, 'orange'), (393, 199, 'orange'), (394, 199, 'orange'), (395, 198, 'orange'), (398, 198, 'orange'), (396, 198, 'orange'), (397, 198, 'orange'), (400, 198, 'orange'), (399, 198, 'orange'), (403, 198, 'orange'), (401, 198, 'orange'), (402, 198, 'orange'), (405, 197, 'orange'), (407, 197, 'orange'), (406, 197, 'orange'), (409, 197, 'orange'), (408, 197, 'orange'), (411, 197, 'orange'), (410, 197, 'orange'), (412, 197, 'orange'), (413, 197, 'orange'), (415, 197, 'orange'), (414, 197, 'orange'), (416, 197, 'orange'), (417, 197, 'orange'), (418, 197, 'orange'), (420, 197, 'orange'), (419, 197, 'orange'), (421, 197, 'orange'), (422, 197, 'orange'), (423, 197, 'orange'), (424, 197, 'orange'), (425, 197, 'orange'), (426, 197, 'orange'), (427, 197, 'orange'), (427, 196, 'orange'), (428, 196, 'orange'), (429, 196, 'orange'), (431, 195, 'orange'), (432, 195, 'orange'), (433, 194, 'orange'), (437, 194, 'orange'), (434, 194, 'orange'), (435, 194, 'orange'), (436, 194, 'orange'), (439, 193, 'orange'), (441, 193, 'orange'), (440, 193, 'orange'), (442, 192, 'orange'), (444, 192, 'orange'), (443, 192, 'orange'), (445, 192, 'orange'), (446, 192, 'orange'), (447, 192, 'orange'), (448, 192, 'orange'), (449, 192, 'orange'), (451, 191, 'orange'), (452, 191, 'orange'), (453, 191, 'orange'), (455, 191, 'orange'), (454, 191, 'orange'), (456, 191, 'orange'), (457, 191, 'orange'), (458, 191, 'orange'), (459, 191, 'orange'), (460, 191, 'orange'), (461, 191, 'orange'), (462, 191, 'orange'), (464, 191, 'orange'), (463, 191, 'orange'), (465, 191, 'orange'), (466, 191, 'orange'), (469, 191, 'orange'), (467, 191, 'orange'), (468, 191, 'orange'), (471, 191, 'orange'), (470, 191, 'orange'), (474, 191, 'orange'), (472, 191, 'orange'), (473, 191, 'orange'), (475, 191, 'orange'), (476, 191, 'orange'), (477, 191, 'orange'), (477, 192, 'orange'), (126, 141, 'brown'), (127, 141, 'brown'), (128, 141, 'brown'), (129, 141, 'brown'), (130, 141, 'brown'), (131, 141, 'brown'), (132, 141, 'brown'), (133, 141, 'brown'), (134, 141, 'brown'), (135, 141, 'brown'), (136, 141, 'brown'), (137, 141, 'brown'), (138, 141, 'brown'), (139, 141, 'brown'), (140, 141, 'brown'), (141, 141, 'brown'), (142, 141, 'brown'), (143, 141, 'brown'), (144, 141, 'brown'), (146, 141, 'brown'), (145, 141, 'brown'), (148, 141, 'brown'), (147, 141, 'brown'), (150, 141, 'brown'), (149, 141, 'brown'), (151, 141, 'brown'), (152, 141, 'brown'), (153, 141, 'brown'), (154, 141, 'brown'), (155, 141, 'brown'), (156, 141, 'brown'), (157, 141, 'brown'), (158, 141, 'brown'), (161, 142, 'brown'), (162, 142, 'brown'), (164, 142, 'brown'), (163, 142, 'brown'), (166, 142, 'brown'), (165, 142, 'brown'), (167, 142, 'brown'), (168, 142, 'brown'), (169, 142, 'brown'), (170, 142, 'brown'), (171, 142, 'brown'), (172, 142, 'brown'), (173, 142, 'brown'), (175, 143, 'brown'), (177, 143, 'brown'), (176, 143, 'brown'), (179, 144, 'brown'), (180, 144, 'brown'), (181, 144, 'brown'), (182, 144, 'brown'), (183, 144, 'brown'), (184, 144, 'brown'), (185, 144, 'brown'), (186, 144, 'brown'), (187, 144, 'brown'), (188, 144, 'brown'), (191, 144, 'brown'), (189, 144, 'brown'), (190, 144, 'brown'), (193, 145, 'brown'), (195, 145, 'brown'), (194, 145, 'brown'), (196, 145, 'brown'), (197, 145, 'brown'), (198, 145, 'brown'), (199, 145, 'brown'), (200, 145, 'brown'), (201, 145, 'brown'), (202, 145, 'brown'), (203, 145, 'brown'), (204, 145, 'brown'), (205, 145, 'brown'), (206, 145, 'brown'), (207, 145, 'brown'), (208, 145, 'brown'), (209, 145, 'brown'), (210, 145, 'brown'), (211, 145, 'brown'), (212, 145, 'brown'), (213, 145, 'brown'), (214, 145, 'brown'), (215, 145, 'brown'), (216, 145, 'brown'), (217, 145, 'brown'), (218, 145, 'brown'), (219, 145, 'brown'), (220, 145, 'brown'), (221, 145, 'brown'), (222, 145, 'brown'), (224, 145, 'brown'), (223, 145, 'brown'), (225, 145, 'brown'), (226, 145, 'brown'), (227, 145, 'brown'), (228, 145, 'brown'), (229, 145, 'brown'), (230, 145, 'brown'), (231, 144, 'brown'), (232, 144, 'brown'), (233, 144, 'brown'), (234, 144, 'brown'), (235, 144, 'brown'), (237, 144, 'brown'), (236, 144, 'brown'), (241, 144, 'brown'), (238, 144, 'brown'), (239, 144, 'brown'), (240, 144, 'brown'), (243, 144, 'brown'), (242, 144, 'brown'), (244, 144, 'brown'), (246, 144, 'brown'), (245, 144, 'brown'), (247, 144, 'brown'), (248, 144, 'brown'), (250, 144, 'brown'), (249, 144, 'brown'), (251, 144, 'brown'), (252, 144, 'brown'), (253, 144, 'brown'), (254, 144, 'brown'), (255, 144, 'brown'), (256, 144, 'brown'), (257, 144, 'brown'), (258, 144, 'brown'), (259, 144, 'brown'), (260, 144, 'brown'), (262, 144, 'brown'), (261, 144, 'brown'), (263, 144, 'brown'), (264, 144, 'brown'), (266, 144, 'brown'), (265, 144, 'brown'), (268, 144, 'brown'), (267, 144, 'brown'), (269, 144, 'brown'), (270, 144, 'brown'), (271, 144, 'brown'), (272, 144, 'brown'), (273, 144, 'brown'), (274, 144, 'brown'), (275, 144, 'brown'), (276, 144, 'brown'), (277, 144, 'brown'), (279, 144, 'brown'), (278, 144, 'brown'), (281, 144, 'brown'), (280, 144, 'brown'), (282, 144, 'brown'), (283, 144, 'brown'), (285, 144, 'brown'), (284, 144, 'brown'), (286, 144, 'brown'), (287, 144, 'brown'), (288, 144, 'brown'), (289, 144, 'brown'), (290, 144, 'brown'), (291, 144, 'brown'), (292, 144, 'brown'), (293, 144, 'brown'), (295, 144, 'brown'), (294, 144, 'brown'), (298, 144, 'brown'), (296, 144, 'brown'), (297, 144, 'brown'), (301, 144, 'brown'), (299, 144, 'brown'), (300, 144, 'brown'), (304, 144, 'brown'), (302, 144, 'brown'), (303, 144, 'brown'), (306, 144, 'brown'), (305, 144, 'brown'), (307, 144, 'brown'), (308, 144, 'brown'), (310, 144, 'brown'), (309, 144, 'brown'), (311, 145, 'brown'), (313, 145, 'brown'), (312, 145, 'brown'), (315, 145, 'brown'), (314, 145, 'brown'), (316, 145, 'brown'), (317, 145, 'brown'), (318, 145, 'brown'), (319, 145, 'brown'), (320, 145, 'brown'), (321, 145, 'brown'), (322, 145, 'brown'), (323, 145, 'brown'), (324, 145, 'brown'), (326, 145, 'brown'), (325, 145, 'brown'), (327, 145, 'brown'), (329, 145, 'brown'), (328, 145, 'brown'), (331, 145, 'brown'), (330, 145, 'brown'), (332, 145, 'brown'), (334, 145, 'brown'), (333, 145, 'brown'), (337, 145, 'brown'), (335, 145, 'brown'), (336, 145, 'brown'), (338, 145, 'brown'), (340, 146, 'brown'), (341, 146, 'brown'), (343, 146, 'brown'), (342, 146, 'brown'), (344, 146, 'brown'), (346, 146, 'brown'), (345, 146, 'brown'), (348, 146, 'brown'), (347, 146, 'brown'), (349, 146, 'brown'), (351, 146, 'brown'), (350, 146, 'brown'), (353, 146, 'brown'), (352, 146, 'brown'), (354, 146, 'brown'), (356, 146, 'brown'), (355, 146, 'brown'), (358, 146, 'brown'), (357, 146, 'brown'), (360, 146, 'brown'), (359, 146, 'brown'), (361, 146, 'brown'), (362, 146, 'brown'), (364, 146, 'brown'), (363, 146, 'brown'), (365, 146, 'brown'), (366, 146, 'brown'), (367, 146, 'brown'), (369, 146, 'brown'), (368, 146, 'brown'), (370, 145, 'brown'), (371, 145, 'brown'), (373, 145, 'brown'), (372, 145, 'brown'), (375, 145, 'brown'), (374, 145, 'brown'), (377, 144, 'brown'), (378, 144, 'brown'), (379, 144, 'brown'), (381, 144, 'brown'), (380, 144, 'brown'), (382, 144, 'brown'), (383, 144, 'brown'), (383, 143, 'brown'), (384, 143, 'brown'), (385, 143, 'brown'), (386, 143, 'brown'), (387, 143, 'brown'), (388, 143, 'brown'), (390, 143, 'brown'), (389, 143, 'brown'), (392, 142, 'brown'), (393, 142, 'brown'), (394, 142, 'brown'), (395, 142, 'brown'), (396, 142, 'brown'), (397, 142, 'brown'), (398, 142, 'brown')]
    #key_letter="C"
    #key_name="Japanese"
    width=10
    colors=["brown","orange","black","purple","green"]
    velocity=100
    notes=collect_notes(Tuple,key_letter,key_name,width,colors)
    #notes={'green': [(39, 55), (40, 55), (43, 55), (56, 55), (56, 55)]}
    #print("1",notes)
    output_midi(notes,velocity)












from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox

# Tonality
root = Tk()
root.title("Tonality")

myLabel1 = Label(root, text= "Choose the tonality first:")
myLabel1.grid()

KEYS = ["A","B","C","D","E","F","G"]
MAJORS = ["major","natural_minor","harmonic_minor","melodic_minor","Chinese","Japanese"]

tonality = StringVar()
tonality.set("C")
ma_or_mi = StringVar()
ma_or_mi.set("major")


def clicked(key,major):
    global mykey,mymajor,west
    tonality = Label(root,text = "Generating music at "+key+" "+major+"!")
    tonality.grid(column=2)
    mykey = key
    mymajor = major
    west = True
    if ma_or_mi.get() == "Chinese" or ma_or_mi.get() == "Japanese":
        west = False
        eastern_canvas()
    else:
        western_canvas()
    show_toolbar()

# Positioning the choices
a=0
for value in KEYS:
    Radiobutton(root,text=value,variable=tonality,value=value).grid(row=1+a,column=0)
    a+=1
a=0
for major in MAJORS:
    Radiobutton(root,text=major,variable=ma_or_mi,value=major).grid(row=1+a,column=1)
    a+=1

tonButton = Button(root, text= "I'm decided",command=lambda:clicked(tonality.get(),ma_or_mi.get()))
tonButton.grid(column=2)

#################################################################
# Functions for drawing (distinguishing w/e -- the canvas is different, thus translating coordinates is different)

def w_draw(event):
    global mylist,color, i
    x, y = event.x, event.y
    if 40<=x<=1240 and 20<=y<=510:
        mylist.append((x-40,510-y,color))
        if canvas.old_coords:
            x1, y1 = canvas.old_coords
            if x!= x1 and y == y1:
                if x>x1:
                    for i in range(1,x-x1,2):
                        mylist.append((x1+i-40,510-y,color))
                else:
                    for i in range(1,x1-x,2):
                        mylist.append((x+i-40,510-y,color))

            elif x == x1 and y != y1:
                if y>y1:
                    for i in range(1,y-y1,2):
                        mylist.append((x-40,510-(y1+i),color))
                else:
                    for i in range(1,y1-y,2):
                        mylist.append((x-40,510-(y+i),color))

            # print(mylist)
            i = canvas.create_line(x, y, x1, y1, width=8, fill = color)
            print(i)
        canvas.old_coords = x, y

# def w_delete():
#     global i
#     if i>253:
#         for j in range(4): 
#             canvas.delete(i)
#             try:
#                 p=mylist.pop()
#             except Exception as e:
#                 print(e)
#             i -= 1
#     elif 249<i<=253:
#         while i>249:
#             canvas.delete(i)
#             try:
#                 p=mylist.pop()
#             except Exception as e:
#                 print(e)
#             i -= 1

def w_clear():
    global i
    while i>249:
        canvas.delete(i)
        i -= 1
    mylist.clear()

def e_draw(event):
    global mylist,color, i
    x, y = event.x, event.y
    if 40<=x<=1240 and 20<=y<=370:
        mylist.append((x-40,370-y,color))
        if canvas.old_coords:
            x1, y1 = canvas.old_coords
            if x!= x1 and y == y1:
                if x>x1:
                    for i in range(1,x-x1,2):
                        mylist.append((x1+i-40,370-y,color))
                else:
                    for i in range(1,x1-x,2):
                        mylist.append((x+i-40,370-y,color))

            elif x == x1 and y != y1:
                if y>y1:
                    for i in range(1,y-y1,2):
                        mylist.append((x-40,370-(y1+i),color))
                else:
                    for i in range(1,y1-y,2):
                        mylist.append((x-40,370-(y+i),color))

            # print(mylist)
            i = canvas.create_line(x, y, x1, y1, width=8, fill = color)
            print(i)
        canvas.old_coords = x, y

# def e_delete():
#     global i
#     if i>239:
#         for j in range(4): 
#             canvas.delete(i)
#             try:
#                 p=mylist.pop()
#             except Exception as e:
#                 print(e)
#             i -= 1
#     elif 235<i<=239:
#         while i>235:
#             canvas.delete(i)
#             try:
#                 p=mylist.pop()
#             except Exception as e:
#                 print(e)
#             i -= 1

def e_clear():
    global i
    while i>235:
        canvas.delete(i)
        i -= 1
    mylist.clear()

def reset_coords(event):
    global i
    canvas.old_coords = None
    i += 1

def go():
    global mykey,mymajor
    # Feed mylist
    # print(mylist)
    # print(mykey,mymajor,mylist)

    main(mylist,mykey,mymajor)


def orange():
    global color
    color = "orange"

def black():
    global color
    color = "black"

def purple():
    global color
    color = "purple"

def brown():
    global color
    color = "brown"

#################################################################
# Toolbar
def show_toolbar():
    global go,clear,piano,violin,cello,flute,recall,v_image,c_image,p_image,f_image,i,mylist,myton,west
    tool = Toplevel()
    tool.title("Toolbar")

    messagebox.showinfo("Warning","KEEP IN MIND:\nWhile drawing lines for violin/cello/flute, please stay in the range of octave I-VI. Drawing at higher octave may result in disturbing/silent notes.")

    v_image = Image.open("violin.png").resize((80,80), Image.ANTIALIAS)
    v_image = ImageTk.PhotoImage(v_image)
    c_image = Image.open("cello.png").resize((80,80), Image.ANTIALIAS)
    c_image = ImageTk.PhotoImage(c_image)

    p_image = Image.open("piano.png").resize((80,80), Image.ANTIALIAS)
    p_image = ImageTk.PhotoImage(p_image)
    f_image = Image.open("flute.png").resize((80,80), Image.ANTIALIAS)
    f_image = ImageTk.PhotoImage(f_image)


    go = Button(tool,text="GO!",width=8,height=2,command=go,foreground="green")
    go.pack(padx=10,pady=20,anchor="n",side="right")

    if west == True:
        clear = Button(tool,text="Clear",width=8,height=2,command=w_clear)
    else:
        clear = Button(tool,text="Clear",width=8,height=2,command=e_clear)
    clear.pack(pady=20,anchor="s",side="right")

    # recall = Button(tool,text="Recall",width=8,height=2,command=w_delete)
    # recall.pack(padx=20,pady=20,anchor="s",side="right")

    piano = Button(tool,image=p_image,command=black)
    piano.pack(padx=10,pady=20,anchor="n",side="left")

    violin = Button(tool,image=v_image,command=orange)
    violin.pack(padx=10,pady=20,anchor="n",side="left")

    cello = Button(tool,image=c_image,command=brown)
    cello.pack(padx=10,pady=20,anchor="n",side="left")

    flute = Button(tool,image=f_image,command=purple)
    flute.pack(padx=10,pady=20,anchor="n",side="left")



#################################################################
# Western Canvas
def western_canvas():
    global canvas,drawing,mylist,i,myton
    mylist = []
    i=0

    drawing = Toplevel()
    drawing.title("Western Canvas")
    canvas = Canvas(drawing, width=1300, height=540)
    canvas.pack()

    for t in range(50):
        canvas.create_line(40,(t+2)*10,1240,(t+2)*10, fill = "grey")
    for j in range(121):
        canvas.create_line((j+4)*10,20,(j+4)*10,510, fill = "grey")

    canvas.create_text(1270,510, text="Time(s)", fill = "grey")
    for k in range(61):
        canvas.create_text((k+2)*20,520, text=k, fill = "grey")

    canvas.create_text(25,12, text="Octave", fill = "grey")
    octave=["VII","VI","V","IV","III","II","I"]
    l = 55
    for num in octave:
        canvas.create_text(20,l, text=num, fill = "grey")
        l += 70

    for i in range(8):
        canvas.create_line(35,20+i*70,40,20+i*70, fill = "grey")

    canvas.old_coords = None
    drawing.bind('<B1-Motion>', w_draw)
    # When releases the click button, clear the "previous" location
    drawing.bind('<ButtonRelease-1>', reset_coords)

#################################################################
# Eastern Canvas
def eastern_canvas():
    global canvas,drawing,mylist,i,myton,west

    mylist = []
    i=0

    drawing = Toplevel()
    drawing.title("Eastern Canvas")
    canvas = Canvas(drawing, width=1300, height=400)
    canvas.pack()

    for t in range(36):
        canvas.create_line(40,(t+2)*10,1240,(t+2)*10, fill = "grey")
    for j in range(121):
        canvas.create_line((j+4)*10,20,(j+4)*10,370, fill = "grey")

    canvas.create_text(1270,370, text="Time(s)", fill = "grey")
    for k in range(61):
        canvas.create_text((k+2)*20,380, text=k, fill = "grey")

    canvas.create_text(25,12, text="Octave", fill = "grey")
    octave=["VII","VI","V","IV","III","II","I"]
    l = 45
    for num in octave:
        canvas.create_text(20,l, text=num, fill = "grey")
        l += 50

    for i in range(8):
        canvas.create_line(35,20+i*50,40,20+i*50, fill = "grey")
    canvas.old_coords = None
    drawing.bind('<B1-Motion>', e_draw)
    drawing.bind('<ButtonRelease-1>', reset_coords)

color = "black" #choose
myton = "C major"
mainloop()












































