(function(){

                
    const form = document.getElementsByTagName('form')[0] 
    let now = {{timeNow |date:"U"}} 
    setInterval(() => {
        makeTimer(
            ({{q_testTaker.timeStart |date:"U"}}+{{q_testTaker.timeLimit}}*60),
            now,
            '.time',
            () =>  {
                form.is_timeout.value = true
                form.submit()
                }
            )
        now += 1
    }, 1000)

    
})() 
