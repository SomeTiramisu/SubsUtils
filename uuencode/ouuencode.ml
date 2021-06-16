exception Pass of int*int*int*int

let pcuu b = output_char stdout (Char.chr (b+33))
let p4b x1 x2 x3 x4 = 
  pcuu x1; 
  pcuu x2; 
  pcuu x3; 
  pcuu x4

let f822 b =
  let c = b lsr 6 in 
  let d = (b lsr 4) land 3 in 
  let e = (b lsr 2) land 3 in 
  let f = b land 3 in 
  c, d, e, f

let f2x326 a b c = (a lsl 4) + (b lsl 2) + c

let f3x824x6 a b c = 
  let a1, a2, a3, a4 = f822 a in 
  let b1, b2,b3, b4 = f822 b in 
  let c1, c2, c3, c4 = f822 c in 
  f2x326 a1 a2 a3, f2x326 a4 b1 b2, f2x326 b3 b4 c1, f2x326 c2 c3 c4

let uuencode ic = 
  let k = ref 0 in
  let rec aux ic= 
    try
    try let a1 = input_byte ic in 
    try let a2 = input_byte ic in
    try let a3 = input_byte ic in
      let x1, x2, x3, x4 = f3x824x6 a1 a2 a3 in raise (Pass (x1, x2, x3, x4))
    with End_of_file ->
      let x1, x2, x3, x4 = f3x824x6 a1 a2 0 in p4b x1 x2 x3 x4
    with End_of_file -> 
      let x1, x2, x3, x4 = f3x824x6 a1 0 0 in p4b x1 x2 x3 x4
    with End_of_file -> ()
    with Pass (x1, x2, x3, x4) -> 
      p4b x1 x2 x3 x4; 
      k := !k+4;
      if (!k mod 80==0 && !k!=0) then (output_char stdout '\n');
      aux ic
    in aux ic

let main () = 
  let file = Sys.argv.(1) in
  let ic = open_in_bin file in 
    uuencode ic;
  flush stdout
;;

main ()
