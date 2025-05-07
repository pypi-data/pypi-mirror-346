from pbdm.psymple_extension.psymple_connections import PBDMCompositeObject, PBDMFunctionalObject, PBDMVariableObject

A = PBDMCompositeObject("A")
B = PBDMCompositeObject("B")
C = PBDMCompositeObject("C")
D = PBDMFunctionalObject("D", assignments=[("q", "14*r*p*t*v")])
E = PBDMVariableObject("E", assignments=[("v", "p*v"), ("u", "2*v")])
F = PBDMCompositeObject("F")
G = PBDMFunctionalObject("G", assignments=[("q", "r+6+p")])
H = PBDMCompositeObject("H")
J = PBDMCompositeObject("J")
K = PBDMVariableObject("K", assignments=[("v", "3*p*v"), ("u", "v")])

objects = [A,B,C,D,E,F,G,H,J, K]

#A.connections={"t": "R.t"}

A.add_children(B, H)
B.add_children(C, F)
C.add_children(D, E)
F.add_children(G)
H.add_children(J)
J.add_children(K)

A.add_input_ports(("r", 1))
B.add_input_ports(("p", 1))
B.add_output_ports("q")
H.add_input_ports("p")
A.add_variable_ports("v")

D.add_output_connection("q", {"C.E.p", "B.q", "B.F.G.p", "A.H.p"})

G.add_output_connection("q", {"B.C.D.t"})

K.add_input_connection("p", "A.B.C.D.q")

D.add_input_connection("v", "A.H.J.K.v")


E.add_variable_connection("v", {"A.H.J.K.v"})

A.add_variable_connection("v", {"B.C.E.v"})

K.add_variable_connection("u", {"A.B.C.E.u"})



A.compile_system_connections()
A.generate_ported_object()