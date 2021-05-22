
const url = window.location.href
const quizbox = document.getElementById('quiz-box')
const scorebox = document.getElementById('score-box')
const resultbox = document.getElementById('result-box')



$.ajax({
	type: 'GET',
	url: `${url}data`,
	error: function(error){
		alert(error)
	},
	success: function(response){
		// console.log(response)
		const data = response.data;
		data.forEach(el=>{
			for(const [questions, answers] of Object.entries(el)){ 
				quizbox.innerHTML += `
						<hr>
						<div class="mb-2">
							<b>${questions}</b>
						</div>
				`

				answers.forEach(answer=>{
						quizbox.innerHTML += `
							<div>
								<input type="radio" class="ans" id="${questions}-${answer}" name="${questions}" value="${answer}">
								<label for="${questions}">${answer}</label>
							</div>
					`
				})
			}
		});
	},
})

const quizForm = document.getElementById('quiz-form')
const quizForm_jquery = $("#quiz-form")
const csrf = document.getElementsByName('csrfmiddlewaretoken')




const sendData = () => {
	const elements = [...document.getElementsByClassName('ans')]
	const data = {}
	data['csrfmiddlewaretoken'] = csrf[0].value
	elements.forEach(el=>{
		if (el.checked){
			data[el.name] = el.value
		}else{
			if(!data[el.name]){
				data[el.name] = null
			}
		}
	})

	$.ajax({
		type : 'POST',
		url : `${url}data/save/`,
		data: data,
		success: function(response){
			// console.log(response)
			const results = response.results
			quizForm_jquery.hide()


			scorebox.innerHTML = `${response.passed ? "Congratulations!": "Ups..( "}Your result is ${response.score.toFixed(2)} %) `


			results.forEach(res=>{
				const resDiv = document.createElement("div")
				for(const [question, resp] of Object.entries(res)){
					resDiv.innerHTML += question
					const cls = ['container', 'p-3', 'text-light', 'h6']
					resDiv.classList.add(...cls)

					if(resp=='not answered'){
						resDiv.innerHTML += '-not answered'
						resDiv.classList.add('bg-danger')
					}
					else if(resp['answered'] == null){
						resDiv.innerHTML += '-not answered'
						resDiv.classList.add('bg-danger')
					}
					else{
						const answer = resp['answered']
						const correct = resp['correct_answer']

						if(answer == correct){
							resDiv.classList.add('bg-success')
							resDiv.innerHTML += ` answered: ${answer}`
						}
						else{
							resDiv.classList.add('bg-danger')
							resDiv.innerHTML += `| correct answer: ${correct}`
							resDiv.innerHTML += `| answered: ${answer}`
						}
					}
				}
				// const body = document.getElementsByTagName('BODY')[0]
				resultbox.append(resDiv)
			})
		},
		error: function(error){
			console.log(error)
		}
	})

}


quizForm.addEventListener('submit', e=>{
	e.preventDefault()



	sendData()
})










