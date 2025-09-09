document.addEventListener("DOMContentLoaded",() => {
  async function get_chapters() {
    console.log("FONCTION EXECUTER")
    chapter?.replaceChildren(optionUndefined)
    // @ts-ignore
    const params = new URLSearchParams();
    // @ts-ignore
    params.append("subject_id",subject.value)

    const response = await fetch(`/panel/api/get/?${params}`);

    const jsonResponse = await response.json();
    
    console.log(jsonResponse)
    jsonResponse.chapters.forEach(element => {
      const option = new Option(element[1],element[0])
      chapter?.appendChild(option)
    });
  }
  
  const grade = document.querySelector("#grade");
  const subject = document.querySelector("#subject");
  const chapter = document.querySelector("#chapter");
  // @ts-ignore
  const optionUndefined = new Option("---------","");
  grade?.addEventListener("change",get_chapters)
  subject?.addEventListener("change",get_chapters)

});