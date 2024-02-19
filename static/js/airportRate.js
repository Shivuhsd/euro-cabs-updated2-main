let result;
// const baseUrl = "http://127.0.0.1:8000/"
let fromCity;

const getDest = async()=> {

    document.getElementById('price').style.display = 'none';

    document.getElementById('booknow').style.display = 'none';

    fromCity = document.getElementById('from')

    const where = document.getElementById('where')

    let domain = window.location.hostname;

    const destUrl = `https://${domain}/airportDest?dest=${fromCity.value}`;


    const response = await fetch(destUrl)
    result = await response.json()

    where.innerHTML = ''


   
    const op = document.createElement('option')
        op.value = 'none'
        op.innerText = 'Select A Destination'

        where.appendChild(op)

    for(let i of result.res)
    {
        const op = document.createElement('option')
        op.value = i.id
        op.innerText = i.airport_name || i.city_name

        where.appendChild(op)
    }

}


const getPrice = async() => {
    const where = document.getElementById('where').value;

    for(let i of result.res )
    {
        if(i.id === where)
        {
            document.getElementById('price').style.display = 'flex';
            document.getElementById('price').style.justifyContent = 'space-between'
            document.getElementById('night').value = `£ ${i.nightRate}`;
            document.getElementById('day').value = `£ ${i.dayRate}`;

            document.getElementById('booknow').style.display = 'block';
        }
    }
}
        
        

                
//         // console.log(result)
             

//         if (result.dest == 'failed')
//         {
//             document.getElementById('price').style.display = 'flex';
//             document.getElementById('price').style.justifyContent = 'space-between'
//             document.getElementById('night').value = "Not Available";
//             document.getElementById('day').value = "Not Available";

//             document.getElementById('booknow').style.display = 'block';
//         }
//         else
//         {
//             for(let i of result.dest )
//             {
//                 document.getElementById('price').style.display = 'flex';
//                 document.getElementById('price').style.justifyContent = 'space-between'
//                 document.getElementById('night').value = `£ ${i.nightRate}`;
//                 document.getElementById('day').value = `£ ${i.dayRate}`;

//                 document.getElementById('booknow').style.display = 'block';
//             }
//         }
//     }

//         else{
//             for(let i of result.dest )
//             {
//                 if(i.id === where)
//                 {
//                     document.getElementById('price').style.display = 'flex';
//                     document.getElementById('price').style.justifyContent = 'space-between'
//                     document.getElementById('night').value = `£ ${i.nightRate}`;
//                     document.getElementById('day').value = `£ ${i.dayRate}`;

//                     document.getElementById('booknow').style.display = 'block';
//                 }
//             }
//         }
//     }catch (E)
//     {
//         console.log("This Destination is Not Available")
//     }  
// }