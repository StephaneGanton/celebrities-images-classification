Dropzone.autoDiscover = false;

function init(){
    let dz = new Dropzone('#dropzone',{
        url:"/",
        maxFiles: 1,
        addRemoveLinks: true,
        dictDefaultMessage: "Some Message",
        autoProcessQueue: false
    });

    dz.on("addedfile", ()=>{
        if(dz.files[1] != null){
            dz.removeFile(dz.files[0]);
        }
    });

    dz.on("complete", (file)=>{
        let imageData = file.dataURL;
        
        var url = "http://127.0.0.1:5000/classify_image"

        $.post(url, {image_data : imageData}, (data, status)=>{
             console.log(data);

             if(!data || data.length==0){
                $("result-holder").hide();
                $("#div-class-table").hide();

                $("#error").show();
             }

            let match = null;
            let bestScore = -1;

            for( let i; i< data.length; i++){
                let maxScoreForThisClass = Math.max(...data[i].class_probability);

                if(maxScoreForThisClass > bestScore){
                    match = data[i];
                    bestScore = maxScoreForThisClass;
                }
            }
            if(match){
                $("#error").hide();
                $("result-holder").show();
                $("#div-class-table").show();

                $("#result-holder").html($(`[data-player="${match.class}"]`).html())

                let classDictionary = match.class_dictionary;

                for(let personName in classDictionary){
                    let index = classDictionary[personName];
                    probabilityScore = match.class_probability[index];
                    let elementName = "#score_" + personName;
                    $(elementName).html(probabilityScore);
                }
            }
        })
    });

    $("#submit-btn").on("click", (e)=>{
        dz.processQueue();
    })
}

$(document).ready(()=>{
    console.log("Dom ready...");
    $("#error").hide();
    $("result-holder").hide();
    $("#div-class-table").hide();

    init();
})