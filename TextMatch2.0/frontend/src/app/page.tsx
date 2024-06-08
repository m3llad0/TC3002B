
export default function Home() {

  return (
    <main className="w-full h-screen bg-white">
      <section className="mx-auto py-20 px-20 flex flex-col justify-center items-center gap-y-8">
        <h1 className=" text-gray-900 text-4xl font-bold">
          Text Match</h1> 
        <div className="flex flex-col gap-y-10 items-center">
          {/* <div className="bg-[#F8FFE5]"> */}

            {/* <button>Text</button>
            <button>File</button> */}
            <textarea
              placeholder="Your paper abstract here ..."
              className="w-[45vw] h-[50vh] mx-10 outline-none focus:outline-none focus:ring-2 text-gray-800 border-2 border-[#06D6A0] rounded-2xl"
              />
            </div>
         
          <button type="button"
            className="text-white bg-[#EF476F] hover:bg-[#EB1E4E] focus:ring-4 focus:outline-none focus:ring-[#F47C98] font-medium rounded-3xl text-sm px-6 py-2.5 text-center md:mr-0 w-fit">
            Enviar</button>
        {/* </div> */}
      </section>
    </main>
  );
}