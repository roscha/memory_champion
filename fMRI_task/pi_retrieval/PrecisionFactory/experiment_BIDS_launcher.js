/* ************************************ */
/* Define experimental variables */
/* ************************************ */

/* action plan

1) define blocks

block 1 : presentation of all cards one by one randomly and randomly position on the screen (or better X position possible)

block 2: all cards one by one for each of the 3 position in a triple (visible cards position)

block 3 : memorise series of triplets of cards without replacement (how many second per triplet)

54 cartes *2 (real fake) *4 (random + action face object spaces) *2 +54/3 (too long)
active double 0 back ? too much mental process 
just full cards 0 back 

does the fake card are use for baseline or for encoding new face actino object? will he make a match ? logical one ? randomizing these symbole doesn't work
or does it ? 

recall on screen : take 10s to remember the next triplet, is this the triplet 


2) define trial types

3) define order of presentation for cards (and define card label : maybe just a list)

4) define position on screen 

5) define label of condition and block and all type of events

6) make X number of design

*/

var exp_lengths = [15, 1 ]; // show all cards, random spots on screen + 1/3 of fake cards // show all cards + 18 same fake cards eually represented in 3 position // (show triplet // show triplet recall next, judge next //)*3




var dirim = './designs/'
var cross = [dirim+'restingstate-01.png'];
jsPsych.pluginAPI.preloadImages(cross);






var counter=[];
for (i=0;i<exp_lengths[0];i++){
	counter.push(i);
}


var counterPop = function(){
	return counter.shift();
}










Intervals=[]
Intervals2=[]
var timingrand = function() {
	var timing=6000
	var interval1=Math.random();
	var interval2=Math.random();
	var interval3=Math.random();
	var interval4=Math.random();
	var tot=interval1+interval2+interval3+interval4;
	
	Intervals.push(interval1/tot*timing,interval2/tot*timing,interval3/tot*timing,interval4/tot*timing);
	Intervals2.push(interval1/tot*timing,interval2/tot*timing,interval3/tot*timing,interval4/tot*timing);
	
};

var itiPop = function() {
	console.log(Intervals);
	return Intervals.shift();
}
var itiPop2 = function() {
	return Intervals2.shift();
}














/* ************************************ */
/* Define experimental variables */
/* ************************************ */


/* ************************************ */
/* Define helper functions */
/* ************************************ */




/* ************************************ */
/* Set up jsPsych blocks */
/* ************************************ */




/* define static blocks  */
//setup experimenter input
var scan_order_setup_block = {
	type: 'survey-text',
	data: {
		trial_id: "scan_order_setup"
	},
	questions: [
		[
			"<p class = center-block-text>Design (0-21):</p>"
		]
	], on_finish: function(data) {
		
		data.scan_order = parseInt(data.responses.split('"')[3])
		
		
		
		
		
		
	}
};


//setup name of output file
var project_name = {
	type: 'survey-text',
	data: {
		trial_id: "project_name"
	},
	questions: [
		[
			"<p class = center-block-text>Project name:</p>"
		]
	], on_finish: function(data) {
		data.project_name = data.responses.split('"')[3]
	}
}
var sub_name = {
	type: 'survey-text',
	data: {
		trial_id: "sub_name"
	},
	questions: [
		[
			"<p class = center-block-text>Subject identifier:</p>"
		]
	], on_finish: function(data) {
		data.sub_name = data.responses.split('"')[3]
	}
};

var session_name = {
	type: 'survey-text',
	data: {
		trial_id: "session_name"
	},
	questions: [
		[
			"<p class = center-block-text>Session:</p>"
		]
	], on_finish: function(data) {
		data.session_name = data.responses.split('"')[3]
	}
};


var run_name = {
	type: 'survey-text',
	data: {
		trial_id: "run_name"
	},
	questions: [
		[
			"<p class = center-block-text>Run number:</p>"
		]
	], on_finish: function(data,filename) {
		data.run_name = data.responses.split('"')[3]
		var date = new Date();
		date = date.getFullYear()+'-'+date.getMonth()+'-'+date.getDate()+'-'+date.getHours()+date.getMinutes();
	
		data.filename = jsPsych.data.getDataByTrialIndex(0).project_name+'_'+jsPsych.data.getDataByTrialIndex(1).sub_name+'_'+jsPsych.data.getDataByTrialIndex(2).session_name+'_'+jsPsych.data.getDataByTrialIndex(3).run_name+'_'+date
		

	}
};


var start_test_block = {
  type: 'poldrack-single-stim',
  stimulus: '<div class = centerbox><div class = center-text>Get ready!<br><br>Stay as still as possible. <br><br>Do not swallow.</div></div>',
  is_html: true,
  choices: 'none',
  timing_stim: 1500, 
  timing_response: 1500,
  data: {
    trial_id: "test_start_block"
  },
  timing_post_trial: 500,
  on_finish: function() {
  	exp_stage = 'test'
  }
};

 var end_block = {
	type: 'poldrack-single-stim',
	stimulus: '<div class = centerbox><div class = center-text><i>Fin</i></div></div>',
	is_html: true,
	choices: [32],
	timing_response: 3000,
	response_ends_trial: true,
	data: {
		trial_id: "end",
		exp_id: 'syncmove'
	},
	timing_post_trial: 0
};


var instructionready = {
  type: 'poldrack-single-stim',
  stimulus: '<div class = instructbox><p class = instruct-text>Get Ready.</p></div>',
  is_html: true,
  choices: 'none',
  timing_response: Math.floor(2000/(TR*1000))*(TR*1000),
  data: {
    trial_id: "instructionready"
  },
  timing_post_trial: 0
};

var instructions_block = {
  type: 'poldrack-single-stim',
  stimulus: '<div class = instructbox><p class = instruct-text>You will see a triplet of digits within a chunk of 5 digits location.<br><br> Think of the triplet representation when they come in first or second positions in the chunk of 5 <br><br> You will then see the full 5-digit chunk : think of the representation and location in the "pi palace"<br><br> <br><br> This will repeat 15times (for a total of 5 min) <br><br> <br><br> You will then be prompted to fixate a cross and recite mentally the 10000 first digits of pi during 10min <br><br> <br><br>  Press SPACE to continue to task</p></div>',
  is_html: true,
  timing_stim: -1, 
  timing_response: -1,
  response_ends_trial: true,
  choices: [32],
  data: {
    trial_id: "instructions",
  },
  timing_post_trial: 0
};

/* ************************************ */
/* Define experimental timeline */
/* ************************************ */



var piretrieval__fmri_experiment = [];



piretrieval__fmri_experiment.push(project_name); //exp_input
piretrieval__fmri_experiment.push(sub_name); //exp_input
piretrieval__fmri_experiment.push(session_name); //exp_input
piretrieval__fmri_experiment.push(run_name); //exp_input
piretrieval__fmri_experiment.push(scan_order_setup_block); //exp_input


piretrieval__fmri_experiment.push(instructions_block); //exp_input


setup_fmri_intro(piretrieval__fmri_experiment);
piretrieval__fmri_experiment.push(start_test_block);

	
	
	var five_ins = {
	  type: 'poldrack-single-stim',
	  stimulus: '<div class = instructbox><p class = instruct-text>You will see a triplet of digits within a chunk of 5 digits location.<br><br> Think of the triplet representation when they come in first or second positions in the chunk of 5 <br><br> You will then see the full 5-digit chunk : think of the representation and location in the "pi palace"</p></div>',
	  is_html: true,
	  choices: 'none',
	  timing_response: 10000,
	  data: {
		trial_id: "5_instruction"
	  },
	  timing_post_trial: 0
	  
	}
	piretrieval__fmri_experiment.push(five_ins);
	
	piretrieval__fmri_experiment.push(instructionready);

for (i=0;i<exp_lengths[0];i++){
	
	
	
	
	
	
	var rest = {
	  type: 'poldrack-single-stim',
	stimulus: '<div class = centerbox><div class = fixation>+</div></div>',
	  is_html: true,
	  choices: 'none',
	  
	  timing_stim: function(){
		 timingrand()
		 return itiPop()+1
	 },
	 timing_response: function() { //use scan_order and timingPop (an iterator) to get correct ITI from ITIs array
			return itiPop2()+1;
		},
	  data: {
		trial_id: "rest"
	  },
	  timing_post_trial: 0,
	  
	}
	piretrieval__fmri_experiment.push(rest);
	
	
	
	
	
	
	
	
	
	
	
	
	var first3 = {
			type: 'poldrack-single-stim',
			stimulus: function(){
				var order = orders[jsPsych.data.getDataByTrialIndex(4).scan_order];
				return '<div class = centerbox><div class = fixation>'+pinumber[order[counter[0]]][0]+'   '+pinumber[order[counter[0]]][1]+'   '+pinumber[order[counter[0]]][2]+'   _   _</div></div>'
			},
			is_html: true,
			choices: 'none',
			data: function(){
				var order = orders[jsPsych.data.getDataByTrialIndex(4).scan_order];
				return {

				trial_id: "second3",
				exp_stage: 'second3',
			pos1: pinumber[order[counter[0]]][0],
			pos2:pinumber[order[counter[0]]][1],
			pos3:pinumber[order[counter[0]]][2],
			pos4:'_',
			pos5:'_'
			}
			},
			timing_post_trial: 0,
			timing_stim: 4000,
					
			timing_response: 4000
		};
		
		
		
		
	
	
	piretrieval__fmri_experiment.push(first3);
		
		
		
		
		
		
		
	
	
	var rest = {
type: 'poldrack-single-stim',
	stimulus: '<div class = centerbox><div class = fixation>+</div></div>',
	  is_html: true,
	  choices: 'none',
	  timing_stim: function(){
		 
		 return itiPop()+1
	 },
	 timing_response: function() { //use scan_order and timingPop (an iterator) to get correct ITI from ITIs array
			return itiPop2()+1;
		},
	  data: {
		trial_id: "rest"
	  },
	  timing_post_trial: 0
	}
	piretrieval__fmri_experiment.push(rest);	
	
	var second3 = {
			type: 'poldrack-single-stim',
			stimulus: function(){
				var order = orders[jsPsych.data.getDataByTrialIndex(4).scan_order];
				return '<div class = centerbox><div class = fixation>_   _   '+pinumber[order[counter[0]]][2]+'   '+pinumber[order[counter[0]]][3]+'   '+pinumber[order[counter[0]]][4]+'</div></div>'
			},
			is_html: true,
			choices: 'none',
			data: function(){
				var order = orders[jsPsych.data.getDataByTrialIndex(4).scan_order];
				return {

				trial_id: "second3",
				exp_stage: 'second3',
			pos1:'_',
			pos2:'_',
			pos3:pinumber[order[counter[0]]][2],
			pos4: pinumber[order[counter[0]]][3],
			pos5: pinumber[order[counter[0]]][4]
			}
			},
			
			
			
			timing_post_trial: 0,
			timing_stim: 4000,
					
			timing_response: 4000
		};
		
		
		
		
	
	
	piretrieval__fmri_experiment.push(second3);
		
		
		
		
	var rest = {
	  type: 'poldrack-single-stim',
	stimulus: '<div class = centerbox><div class = fixation>+</div></div>',
	is_html: true,
	  choices: 'none',
	  timing_stim: function(){
		 
		 return itiPop()+1
	 },
	 timing_response: function() { //use scan_order and timingPop (an iterator) to get correct ITI from ITIs array
			return itiPop2()+1;
		},
	  data: {
		trial_id: "rest"
	  },
	  timing_post_trial: 0
	}
	piretrieval__fmri_experiment.push(rest);	
	
	
	
	var full5 = {
			type: 'poldrack-single-stim',
			
			stimulus: function(){
				var order = orders[jsPsych.data.getDataByTrialIndex(4).scan_order];
				return '<div class = centerbox><div class = fixation>'+pinumber[order[counter[0]]][0]+'   '+pinumber[order[counter[0]]][1]+'   '+pinumber[order[counter[0]]][2]+'   '+pinumber[order[counter[0]]][3]+'   '+pinumber[order[counter[0]]][4]+'</div></div>'
			},
			is_html: true,
			choices: 'none',
			data: function(){
				var order = orders[jsPsych.data.getDataByTrialIndex(4).scan_order];
				return {

				trial_id: "full5",
				exp_stage: 'full5',
			pos1:pinumber[order[counter[0]]][0],
			pos2:pinumber[order[counter[0]]][1],
			pos3:pinumber[order[counter[0]]][2],
			pos4: pinumber[order[counter[0]]][3],
			pos5: pinumber[order[counter[0]]][4]
			}
			},
			
			
			
			timing_post_trial: 0,
			timing_stim: 6000,
					
			timing_response: 6000
		};
		
		
		
		
	
	
	piretrieval__fmri_experiment.push(full5);
		
		
		
		
		
		
	var rest = {
	  type: 'poldrack-single-stim',
	stimulus: '<div class = centerbox><div class = fixation>+</div></div>',
	is_html: true,
	  choices: 'none',
	  timing_stim: function(){
		 
		 return itiPop()+1
	 },
	 timing_response: function() { //use scan_order and timingPop (an iterator) to get correct ITI from ITIs array
			return itiPop2()+1;
		},
	  data: {
		trial_id: "rest"
	  },
	  timing_post_trial: 0,
	  on_finish:function(){
		  
		  
		  counterPop()
		  //fetch("https://dosenbachlab.wustl.edu/services/json", { method: "POST", headers: { "Content-type": "application/json" }, body: JSON.stringify({ filename: "public/piretrieval/results/"+jsPsych.data.getDataByTrialIndex(3).filename+".json", data: jsPsych.data.dataAsJSON() })}).then( data => data.json() ).then( data => console.log(data) );
		  
	  }
	}
	piretrieval__fmri_experiment.push(rest);	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	}
	
	
	
	
	
	
	
	
	
	
	
	
	
	var recite_ins = {
	  type: 'poldrack-single-stim',
	  stimulus: '<div class = instructbox><p class = instruct-text>You will see a cross, fixate the cross and recite the 10000 first digits of pi during the following 10min.</p></div>',
	  is_html: true,
	  choices: 'none',
	  timing_response: 7000,
	  data: {
		trial_id: "recite_instruction"
	  },
	  timing_post_trial: 0
	  
	}
	
	piretrieval__fmri_experiment.push(recite_ins);
	piretrieval__fmri_experiment.push(instructionready);
	
	var recite = {
	  type: 'poldrack-single-stim',
	  stimulus: '<div class = centerbox><div class = fixation>+</div></div>',
	  is_html: true,
	  choices: 'none',
	  timing_response: 599964,
	  data: {
		trial_id: "recite"
	  },
	  timing_post_trial: 0
	}
	piretrieval__fmri_experiment.push(recite);
	



//end
piretrieval__fmri_experiment.push(end_block);



