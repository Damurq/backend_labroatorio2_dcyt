/* eslint-disable */
const defaultObject = {
    info: {
        count: 0,
        next: null,
        pages: 0
    },
    results: []
};


/**
 * 
 * @param {*} url 
 * @returns 
 */
async function request(url) {
    try {
        const response = await fetch(url)
        if (!response.ok) {
            return defaultObject
        }
        else {
            const data = await response.text();
            const json = JSON.parse(data);
            return json;
        }
    }
    catch (e) {
        return defaultObject
    }
}
/**
 * 
 * @param {*} labels 
 * @param {*} data 
 * @returns 
 */
function filterDataTable(labels, data) {
    let newData = data.map((obj) => {
        let objData = {}
        labels.forEach((label) => {
            objData[label] = obj[label];
        })
        return objData;
    })
    return newData
}

/**
 * 
 * @param {*} urlBase 
 * @param {*} schema 
 * @param {*} filters 
 */
async function filterD(urlBase = "", schema = "", filters = {}) {
    let newUrl = urlBase + schema
    Object.keys(filters).forEach((element, index) => {
        if (index == 0) {
            newUrl += "/?" + element + "=" + filters[element];
        }
        else {
            newUrl += "&" + element + "=" + filters[element];
        }
    })
    let data = await request(newUrl)
    //console.log(newUrl)
    return data
}

async function getAll(urlBase = "", schema = "", labels) {
    let info = []
    let next = typeof urlBase === "string" ? urlBase + schema : null
    while (next !== null) {
        let data = await request(next)
        next = data.info.next
        info.push(...filterDataTable(labels, data.results));
    }
    return info;
}

async function character() {
    let data = await request("http://127.0.0.1:8000/users/list/")
    return data
}

async function episode() {
    let data = await request("https://rickandmortyapi.com/api/episode")
    return data.results
}

async function getDataBar(section, labels, label) {
    let result = await getAll("https://rickandmortyapi.com/api/", section, labels)
    let dta = result.map((d) => d[label])
    return dta

}
let fdt = [] //programas
let fdt2 =[] //pensum
let fdt3 = [] //
let programC =[] //programas temporales
let url = "http://127.0.0.1:8000/api/program/list/"
request(url)
.then((response) => {
    if (response.length > 0) {
        fdt = filterDataTable(["code", "name"], response);
        let url2 = "http://127.0.0.1:8000/api/pensum/list/"
        request(url2)
        .then((response) => {
            if (response.length > 0) {
                fdt2 = filterDataTable(["program_code"], response);
                fdt3 = fdt.map((obj)=>{
                    programC.push({program_code:obj["code"]})
                    return ({
                        code:obj["code"],
                        name:obj["name"],
                        cantidad:0
                    })
                })
                fdt2.forEach((obj)=>{

                    //     temporalData[programC.indexOf(val)]++;
                    // }
                    // obj["program_code"]
                })
            }
        })
    }
})

// character().then(function (data) {
//     console.log("bien")
//     console.log(data)
//     const $div = document.getElementById("root")
//     let source = () => {
//         let texto = ""
//         let s = data.map((src) => {
//             return src["photo"]
//         })
//         content = s.map((src) => {
//             return "<picture><img src='" + "http://127.0.0.1:8000" + src + "' alt=''></picture>"
//         })
//         content.forEach((e)=>{
//             texto +=e
//         } )
//         return texto
//     }
//     $div.innerHTML += source()
// }, function (reason) {
//     console.log("mal")
//     console.log(reason)
// });


module.exports = {
    getDataBar,
    request,
    filterD,
    getAll,
    character,
    episode,
    filterDataTable
}