from pydub import AudioSegment
import audio_crop
import os
import numpy
import pandas as pd

def breath_annot_extractor(annotation_file):
	#creates a list of list where in each list has the start and stop timings of only specified annotations, here it's ii/xx 		
	subject_breath_annotation = []
	fr = open(annotation_file)
	lines = fr.readlines()
	for line in lines:
		line = line.strip("\n").split("\t")
		if (line[2].strip() == "ii") or (line[2].strip() == "xx"):
			subject_breath_annotation.append([ float(line[0]), float(line[1]) ])
	return subject_breath_annotation
	

def trim_audio(input_file_path, output_file_name, subject_breath_annotation):
	# load the audio file
	audio = AudioSegment.from_file(input_file_path)
	# iterate over the list of time intervals
	j=0
	for i, (start_time, end_time) in enumerate(subject_breath_annotation):
		# extract the segment of the audio
		segment = audio[start_time*1000:end_time*1000]
		if(j==0): #for the first audio segment
			output_file_name = output_file_name + ".wav"
			segment.export(output_file_name, format='wav')
			wav_file_1 = AudioSegment.from_file(output_file_name)
			j=1
		else: #for subsequent audio segments, append the previous extracted results iteratively.
			wav_file_2_name = "working.wav" #ignore this file at the end
			segment.export(wav_file_2_name, format='wav')
			wav_file_2 = AudioSegment.from_file(wav_file_2_name)
			wav_file_1 = wav_file_1 + wav_file_2	
		#print(segment.get_array_of_samples())
		# construct the output file path
		#output_file_path_i = f"{subjects[0]}_{i}.wav"
		# export the segment to a file
		#segment.export(output_file_path_i, format='wav')
	wav_file_1.export(output_file_name, format='wav')
	return
	
subject_breath_annotation = breath_annot_extractor(r"annotation_text_file_path_here")
input_file_path = (r"audio_file_path_here")
trim_audio(input_file_path, "extracted_1", subject_breath_annotation) #final extracted audio file"
print("...done!")




