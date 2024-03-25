       /**
        Javascript code
       */
        const dropArea = document.querySelector(".drag-area");
        const dragText = document.querySelector(".header");
        let button = dropArea.querySelector(".button");
        let input = dropArea.querySelector("input");
        let file;
        let imgTag;


        button.onclick = () => {
            input.click();
        };
        // when browse
        input.addEventListener("change", function () {
            file = this.files[0];
            dropArea.classList.add("active");
            displayFile();
        });

        // when file is inside drag area but not leaved inside it 
        dropArea.addEventListener("dragover", (event) => {
            event.preventDefault();
            dropArea.classList.add("active");
            dragText.textContent = "Release to Upload";
            // console.log('File is inside the drag area');
        });

        // when file leave the drag area
        dropArea.addEventListener("dragleave", () => {
            dropArea.classList.remove("active");
            // console.log('File left the drag area');
            dragText.textContent = "Drag & Drop";
        });

        // when file is dropped on the drag area
        dropArea.addEventListener("drop", (event) => {
            event.preventDefault();
            // console.log('File is dropped in drag area');
            file = event.dataTransfer.files[0]; // grab single file even of user selects multiple files
            alert(file.name);
            displayFile();
        });
        
        function displayFile() {
            let fileType = file.type;
            //alert(file.type)
            // console.log(fileType);
            let validExtensions = ["image/jpeg", "image/jpg", "image/png", "video/mp4"];
            if (validExtensions.includes(fileType)) {
                // console.log('This is an image file');
                let fileReader = new FileReader();
                fileReader.onload = () => {
                    let fileURL = fileReader.result;
                    console.log(fileURL);
                    if(fileType.split("/")[0] == "image"){
                        imgTag = `<img src="${fileURL}" alt="" id="uploaded-img">`;
                    } else {
                        imgTag = '<video height="100%" controls="controls">\n<source src="'+fileURL+'" type="video/mp4" />\n</video>';
                    }
                    //alert(imgTag)
                    dropArea.innerHTML = imgTag;
                };
                fileReader.readAsDataURL(file);
            } else {
                alert("This is not an Image File");
                dropArea.classList.remove("active");
            }
            
        }

        function uploadFile(){
            //alert(file.type.split("/")[0])
            //var file = document.getElementById('fileInput').files[0];
            if(file){
                const fileType = file.type.split("/")[0]
                const fileName = file.name
                var destUrl = 'http://192.168.1.112:8080/upload_image'
                var hrefUrl = 'http://192.168.1.112:8080/show_prediction'
                const formData = new FormData();
                formData.append('file', file);
                //formData.append('type', fileType)
                
                
                fetch(destUrl, {
                       method: 'POST',
                       body: formData,
                       redirect: 'follow'
                     })
                     .then(async response => {
                       console.log(await response.text());
                       window.location.href = hrefUrl;
                     })
                     .catch(error => {
                       console.error(error);
                     });
                
            }else{
                alert("Nessun file selezionato");
            }
        }