
var exp_len = 44;
/* Instruction Prompt */
var possible_responses = [
	["index finger", 89],
	["middle finger", 66]
	
]
// set up responses
var choices = [possible_responses[0][1], possible_responses[1][1]]




//////// set up experiment blocks


// need to check what data I want to save (specially corect answer)
// need to finish creating 01 answer
//fix button
// fix size
// less time for word
//verify bay3 ok

choicesCounter=[];
choicesCounter2=[];
choicesCounterBIS2=[];
choicesCounter3=[];
choicesCounter4=[];
choicesCounterBIS4=[];
choicesCounter5=[];
choicesCounter6=[];
sentencesCounter=[];
testCounter=[];
wordsCounter=[];
orderCounter=[];
orderCounter2=[];
timingCounter=[];
timingCounter2=[];
timingCounter3=[];
timingCounter4=[];
timingCounter5=[];
timingCounter6=[];
for (i=0;i<exp_len;i++){
	choicesCounter.push(i);
	choicesCounter2.push(i);
	choicesCounterBIS2.push(i);
	choicesCounter3.push(i);
	choicesCounter4.push(i);
	choicesCounterBIS4.push(i);
	choicesCounter5.push(i);
	choicesCounter6.push(i);
	sentencesCounter.push(i);
	testCounter.push(i);
	wordsCounter.push(i);

	timingCounter.push(i);
	timingCounter2.push(i);
	timingCounter3.push(i);
	timingCounter4.push(i);
	timingCounter5.push(i);
	timingCounter6.push(i);
}
for (i=0;i<orders[0].length;i++){
	orderCounter.push(i);
	orderCounter2.push(i);
}


var choicesPop = function() {
	return choicesCounter.shift();
}
var choicesPop2 = function() {
	return choicesCounter2.shift();
}
var choicesPopBIS2 = function() {
	return choicesCounterBIS2.shift();
}
var choicesPop3 = function() {
	return choicesCounter3.shift();
}
var choicesPop4 = function() {
	return choicesCounter4.shift();
}
var choicesPopBIS4 = function() {
	return choicesCounter4.shift();
}
var choicesPop5 = function() {
	return choicesCounter5.shift();
}
var choicesPop6 = function() {
	return choicesCounter6.shift();
}
var sentencesPop = function() {
	return sentencesCounter.shift();
}
var testPop = function() {
	return testCounter.shift();
}
var wordsPop = function() {
	return wordsCounter.shift();
}
var orderPop = function() {
	return orderCounter.shift();
}
var orderPop2 = function() {
	return orderCounter2.shift();
}
var timingPop = function() {
	return timingCounter.shift();
}
var timingPop2 = function() {
	return timingCounter2.shift();
}
var timingPop3 = function() {
	return timingCounter3.shift();
}
var timingPop4 = function() {
	return timingCounter4.shift();
}
var timingPop5 = function() {
	return timingCounter5.shift();
}
var timingPop6 = function() {
	return timingCounter6.shift();
}
//first practice block
practice_loop=[]
practice_sentences=['Andy loved to sleep on a bed of tails.','She was too small to see over the fence.','The bread market is fishing on a low tide.'];
practice_judge2=[1,0,1];
practice_judge=[0,1,1];
practice_word=['tree','chart','glasses'];
practice_test_word=['tree','cat','lences'];
practice_test_judge=[0,1,1];
practice_test_judge2=[0,1,1];
var practice_sentencesPop = function() {
	return practice_sentences.shift();
}
var practice_judgePop2 = function() {
	return practice_judge2.shift();
}
var practice_judgePop = function() {
	return practice_judge.shift();
}
var practice_wordPop = function() {
	return practice_word.shift();
}
var practice_test_judgePop = function() {
	return practice_test_judge.shift();
}
var practice_test_wordPop = function() {
	return practice_test_word.shift();
}
var practice_test_judgePop2 = function() {
	return practice_test_judge2.shift();
}


for (i=0;i<3;i++){
	var practice_block = {type: 'poldrack-categorize',
			key_answer: choices[practice_judgePop2()],
			data: {phase: 'practice', response: choices[practice_judgePop()]},
			stimulus: '<div class = centerbox><div class = center-text><div class=ss_stim>'+practice_sentencesPop()+'</div></div></div>',	
			is_html: true,
			choices: choices,
			  timing_response: 7000,
			  
			  response_ends_trial: true,
			  
			  correct_text: '<div class = feedbackbox><div style="color:#4FE829"; class = center-text>Correct!</p></div>',
			incorrect_text: '<div class = feedbackbox><div style="color:red"; class = center-text>Incorrect</p></div>',
			timeout_message: '<div class = feedbackbox><div class = center-text>Too Slow</div></div>',
			show_stim_with_feedback: false,
			timing_feedback_duration: 500,
			on_finish: function(data) {
				jsPsych.data.addDataToLastTrial({
					exp_stage: 'practice',
					
				})
			}
	};
	practice_loop.push(practice_block);
	var practice_block2 = {
		  type: "poldrack-single-stim",
		  stimulus: '<div class = feedbackbox><div class = center-text><div class=ss_stim>'+practice_wordPop()+'</div></div></div>',
		  choices: 'None', timing_response: 1500, data: {phase: 'mem'}, data: {phase: 'mem_pra'},
		  is_html: true,
		  on_finish: function(data) {
						jsPsych.data.addDataToLastTrial({
							exp_stage: 'practice',
							/// and more
							
						})
		  }
	};
	practice_loop.push(practice_block2);
	
};
// recall block (???)
var recall_block_practice = {
  type: "poldrack-single-stim",
  stimulus: '<div class = feedbackbox><div class = center-text>???</div></div>',
  is_html: true,
  choices: 'none',
  timing_response: 7000,
  data: {
    trial_id: "practice_recall"
  },
  
};
practice_loop.push(recall_block_practice);


for (i=0;i<3;i++){
	var practice_test = {type: 'poldrack-categorize',
			key_answer: choices[practice_test_judgePop()],
			data: {phase: 'practice', response: choices[practice_test_judgePop2()]},
			stimulus: '<div class = feedbackbox><div class = center-text><div class=ss_stim>'+practice_test_wordPop()+' ?</div></div></div>',	
			is_html: true,
			choices: choices,
			  timing_response: 2000,
			  
			  response_ends_trial: true,
			  
			  correct_text: '<div class = feedbackbox><div style="color:#4FE829"; class = center-text>Correct!</p></div>',
			incorrect_text: '<div class = feedbackbox><div style="color:red"; class = center-text>Incorrect</p></div>',
			timeout_message: '<div class = feedbackbox><div class = center-text>Too Slow</div></div>',
			show_stim_with_feedback: false,
			timing_feedback_duration: 500,
			on_finish: function(data) {
				jsPsych.data.addDataToLastTrial({
					exp_stage: 'practice',
					
				})
			}
	};
	practice_loop.push(practice_test);
	
	
};



var pre_if_practice = {
	type: 'poldrack-text',
	data: {
		trial_id: "practice_question"
	},
	timing_response: 180000,
	text: '<div class = centerbox><p class = center-block-text> Press S to skip the practice, or V to view it.</p></div>',
	cont_key: [83,86],
	timing_post_trial: 1000,
	on_finish: function() {
		exp_stage = 'test'
	}
};

var if_practice = {
    timeline: practice_loop,
    conditional_function: function(){
        // get the data from the previous trial,
        // and check which key was pressed
        var ifdata = jsPsych.data.getDataByTrialIndex(9);//jsPsych.data.get().last(1).values()[0];
		console.log(ifdata.key_press);
        if(ifdata.key_press==83){//jsPsych.pluginAPI.compareKeys(ifdata.key_press, 's')){
            return false;
        } else {
            return true;
        }
    }
}


//////////////////////////////
var post_trial_gap = function(iti) {
	var curr_trial = jsPsych.progress().current_trial_global
	return 6750 - jsPsych.data.getData()[curr_trial - 1].block_duration + get_ITI(iti)
};



var get_ITI = function(iti) {
	return  iti/2*1000 + 250
};
var post_word_test_gap = function(iti) {
	var curr_trial = jsPsych.progress().current_trial_global
	return 2000 - jsPsych.data.getData()[curr_trial - 1].block_duration + iti*1000
};	

var recall_block = {
  type: "poldrack-single-stim",
  stimulus: '<div class = feedbackbox><div class = center-text>???</div></div>',
  is_html: true,
  choices: 'none',
  timing_post_trial: 0,
  timing_response: Math.floor(7000/(TR*1000))*(TR*1000),
  data: {
    trial_id: "recall"
  },
  
};


var sentences_block = {type: 'poldrack-single-stim',
			key_answer: function(){
				var scan_order = jsPsych.data.getDataByTrialIndex(4).scan_order;
			return choices[sentence_judge[scan_order][choicesPop()]]},	
			
			data: function(){
				var scan_order = jsPsych.data.getDataByTrialIndex(4).scan_order;
				
				return {phase: 'test', NoneSense:sentence_judge[scan_order][choicesPopBIS2()],  response: choices[sentence_judge[scan_order][choicesPop2()]]}},
			stimulus: function(){
				var scan_order = jsPsych.data.getDataByTrialIndex(4).scan_order;
			return '<div class = centerbox><div class = center-text><div class=ss_stim>'+sentences[scan_order][sentencesPop()]+'</div></div></div>'},	
			is_html: true,
			choices: choices,
			timing_post_trial: 0,
			  timing_response: 6750,
			  
			  response_ends_trial: true,
			  
			
			on_finish: function(data) {
				
				correct = false
				if (data.key_press == data.response) {
				correct = true
				}
				jsPsych.data.addDataToLastTrial({
					trial_id: "sentence",
					exp_stage: 'test',
					correct: correct
					
				})
			}
};
var fixation_sentences = {
			type: 'poldrack-single-stim',
			stimulus: '<div class = centerbox><div class = center-text>+</div></div>',
			is_html: true,
			choices: 'none',
			data: {

				trial_id: "fixation",
				exp_stage: 'test'
			},
			timing_post_trial: 0,
			timing_stim: function() { //use scan_order and timingPop (an iterator) to get correct ITI from ITIs array
						var itiprov = ITIs[jsPsych.data.getDataByTrialIndex(4).scan_order];
						return post_trial_gap(itiprov[timingPop()]);    
					},
					
			timing_response: function() { //use scan_order and timingPop (an iterator) to get correct ITI from ITIs array
						var itiprov = ITIs[jsPsych.data.getDataByTrialIndex(4).scan_order];
						return post_trial_gap(itiprov[timingPop2()]);   
					} // 0 or should be same time as timing_stim?
};
var word_block = {
		  type: "poldrack-single-stim",
		  stimulus: function(){
				var scan_order = jsPsych.data.getDataByTrialIndex(4).scan_order;
				
				return '<div class = feedbackbox><div class = center-text><div class=ss_stim>'+words[scan_order][wordsPop()]+'</div></div></div>'},
		  choices: 'None', timing_response: 1250, data: function(){
				var scan_order = jsPsych.data.getDataByTrialIndex(4).scan_order;
				
		  return {phase: 'mem', order : orders[scan_order][orderCounter[0]]}},
		  is_html: true,
		  timing_post_trial: 0,
		  on_finish: function(data) {
						jsPsych.data.addDataToLastTrial({
							trial_id: "mem",
							exp_stage: 'test',
							/// and more
							
						})
						
			//fetch("https://dosenbachlab.wustl.edu/services/json", { method: "POST", headers: { "Content-type": "application/json" }, body: JSON.stringify({ filename: "public/readingspan/results/"+jsPsych.data.getDataByTrialIndex(3).filename+".json", data: jsPsych.data.dataAsJSON() })}).then( data => data.json() ).then( data => console.log(data) );
	
		  }
};
var fixation_word = {
			type: 'poldrack-single-stim',
			stimulus: '<div class = centerbox><div class = center-text>+</div></div>',
			is_html: true,
			choices: 'none',
			data: {

				trial_id: "fixation",
				exp_stage: 'test'
			},
			timing_post_trial: 0,
			timing_stim: function() { //use scan_order and timingPop (an iterator) to get correct ITI from ITIs array
						var itiprov = ITIs[jsPsych.data.getDataByTrialIndex(4).scan_order];
						return get_ITI(itiprov[timingPop3()]);    
					},
					
			timing_response: function() { //use scan_order and timingPop (an iterator) to get correct ITI from ITIs array
						var itiprov = ITIs[jsPsych.data.getDataByTrialIndex(4).scan_order];
						return get_ITI(itiprov[timingPop4()]);   
					} // 0 or should be same time as timing_stim?
};




var word_test = {type: 'poldrack-single-stim',
			key_answer: function(){
				var scan_order = jsPsych.data.getDataByTrialIndex(4).scan_order;
			return choices[words_judge[scan_order][choicesPop3()]]},
			data: function(){
				var scan_order = jsPsych.data.getDataByTrialIndex(4).scan_order;
				
			return {phase: 'test', w_test:words_judge[scan_order][choicesPopBIS4()], response: choices[words_judge[scan_order][choicesPop4()]], order : orders[scan_order][orderCounter2[0]]}},
				
			stimulus: function(){
				var scan_order = jsPsych.data.getDataByTrialIndex(4).scan_order;
			return '<div class = feedbackbox><div class = center-text><div class=ss_stim>'+words_test[scan_order][testPop()]+' ?</div></div></div>'},	
			
			is_html: true,
			choices: choices,
			timing_post_trial: 0,
			  timing_response: 1900,
			  
			  response_ends_trial: true,
			
			on_finish: function(data) {
				correct = false
				if (data.key_press == data.response) {
				correct = true
				}
				jsPsych.data.addDataToLastTrial({
					exp_stage: 'test',
					correct : correct
				})
				//fetch("https://dosenbachlab.wustl.edu/services/json", { method: "POST", headers: { "Content-type": "application/json" }, body: JSON.stringify({ filename: "public/readingspan/results/"+jsPsych.data.getDataByTrialIndex(3).filename+".json", data: jsPsych.data.dataAsJSON() })}).then( data => data.json() ).then( data => console.log(data) );
			}
};
	
var fixation_word_test = {
			type: 'poldrack-single-stim',
			stimulus: '<div class = centerbox><div class = center-text>+</div></div>',
			is_html: true,
			choices: 'none',
			data: {

				trial_id: "fixation",
				exp_stage: 'test'
			},
			timing_post_trial: 0,
			timing_stim: function() { //use scan_order and timingPop (an iterator) to get correct ITI from ITIs array
						var itiprov = ITIs[jsPsych.data.getDataByTrialIndex(4).scan_order];
						return post_word_test_gap(itiprov[timingPop5()]);    
					},
					
			timing_response: function() { //use scan_order and timingPop (an iterator) to get correct ITI from ITIs array
						var itiprov = ITIs[jsPsych.data.getDataByTrialIndex(4).scan_order];
						return post_word_test_gap(itiprov[timingPop6()]);   
					} // 0 or should be same time as timing_stim?
};
var count=1;
var test_timeline1={
	timeline : [word_block,fixation_word,sentences_block,fixation_sentences],
	loop_function: function(data){
		var scan_order = jsPsych.data.getDataByTrialIndex(4).scan_order;
        if(orders[scan_order][orderCounter[0]]==count){
			orderPop();
			count=1;
            return false;
        } else {
			count++;
            return true;
        }
    }
		
}

var test_timeline2={
	timeline : [word_test,fixation_word_test],
	loop_function: function(data){
		var scan_order = jsPsych.data.getDataByTrialIndex(4).scan_order;
        if(orders[scan_order][orderCounter2[0]]==count){
			orderPop2();
			count=1;
            return false;
        } else {
			count++;
            return true;
        }
    }
}



////// set up intro wrapper blocks



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
}

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
}


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
}


var scan_order_setup_block = {
	type: 'survey-text',
	data: {
		trial_id: "scan_order_setup"
	},
	questions: [
		[
			"<p class = center-block-text>Design (0-29):</p>"
		]
	], on_finish: function(data) {
		
		data.scan_order = parseInt(data.responses.split('"')[3]);
		var order = orders[data.scan_order];
			
	}
}


//instructions 


var instructions_block = {
  type: 'poldrack-single-stim',
  stimulus: '<div class = instructbox><p class = instruct-text>The following task consists of two parts. First, you will see sentences on the screen, which you are supposed to read silently. These sentences can make sense (e.g. <i>More and more women want to have a career.</i>) or not (e.g. <i>I stopped by the gas station to refuel on apple juice.</i>). Your first task is to judge the content of each sentence. You will do this by pressing a key to indicate whether it makes sense or not. <br><br>'+possible_responses[0][0]+' = yes<br><br> '+possible_responses[1][0]+' = no<br><br> After this decision you will see a word on the screen, which you are also supposed to read silently. Your second task is to memorise this word in order to recall it later on.</p><p class = instruct-text> Please press SPACE to continue.</p></div>',
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

var instructions_block2 = {
  type: 'poldrack-single-stim',
  stimulus: '<div class = instructbox><p class = instruct-text>After three to seven sentences (which you are supposed to judge) and words (which you are supposed to memorise), you will see three question marks (<i>???</i>). Whenever this happens, please silently recall all words you still remember from the set <i>???</i>.<br><br> Then you will see the words from the list again presented one by one with a "?", some of them will be wrong. You will judge if you remember that the word was in the list <br><br>'+possible_responses[0][0]+' = yes <br><br> '+possible_responses[1][0]+' = no. </p><p class = instruct-text> Please press SPACE to continue to the practice.</p></div>',
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





var rest_block = {
  type: 'poldrack-single-stim',
  stimulus: '<div class = centerbox><div class = center-text>Next run will start in a moment</div></div>',
  is_html: true,
  choices: 'none',
  timing_response: Math.floor(7000/(TR*1000))*(TR*1000),
  data: {
    trial_id: "rest_block"
  },
  timing_post_trial: Math.floor(1000/(TR*1000))*(TR*1000)
};

var shortrest_block = {
  type: 'poldrack-single-stim',
  stimulus: '<div class = centerbox><div class = center-text>New set</div></div>',
  is_html: true,
  choices: 'none',
  timing_response: Math.floor(2000/(TR*1000))*(TR*1000),
  data: {
    trial_id: "transition_block"
  },
  timing_post_trial: Math.floor(1000/(TR*1000))*(TR*1000)
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
		exp_id: 'readingspan'
	},
	timing_post_trial: 0
};








/* ************************************ */
/* Set up experiment */
/* ************************************ */
//timeline structure
var readingspan_experiment = [];
readingspan_experiment.push(project_name); //exp_input
readingspan_experiment.push(sub_name); //exp_input
readingspan_experiment.push(session_name); //exp_input
readingspan_experiment.push(run_name); //exp_input
readingspan_experiment.push(scan_order_setup_block); //exp_input


test_keys(readingspan_experiment, choices);
readingspan_experiment.push(instructions_block);
readingspan_experiment.push(instructions_block2);


readingspan_experiment.push(pre_if_practice);
readingspan_experiment.push(if_practice);


setup_fmri_intro(readingspan_experiment);


			
for (o=0;o<orders[0].length;o++){
	readingspan_experiment.push(test_timeline1);
	readingspan_experiment.push(recall_block)
	readingspan_experiment.push(test_timeline2);
	
	//if (o==orders[0].length/2){
	//	readingspan_experiment.push(rest_block);
	//}else{
		readingspan_experiment.push(shortrest_block);
	//}
}



//readingspan_experiment.push(if_test);
//readingspan_experiment.push(wtest_loop);
//
readingspan_experiment.push(end_block);