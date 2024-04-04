import os
import pytacs
from tacs_orig import functions, constitutive


def setup(bdfFile, output, comm=None):
    structOptions = {
        "gravityVector": [0, -9.81, 0],
        "projectVector": [0, 1, 0],  # normal to planform
        "outputDir": output,
        # "transferfileName": "transfer",  # output rigid links
    }
    FEASolver = pytacs.pyTACS(bdfFile, comm=comm, options=structOptions)

    # rst end setup_tacs-init

    # ==============================================================================
    #       Set up design variable groups
    # ==============================================================================
    # Give each rib its own design variable group under the 'RIBS' category
    for i in range(1, 19):
        FEASolver.addDVGroup("RIBS", include=f"RIB.{i:02}")

    # rst end setup_tacs-ribDVs

    # Split each spar into 9 design variable groups
    FEASolver.addDVGroup("SPARS", include="SPAR.00", nGroup=9)
    FEASolver.addDVGroup("SPARS", include="SPAR.09", nGroup=9)

    # rst end setup_tacs-sparDVs

    # Now create the skin groups, from side of body outwards, 2 skin panels per group
    for skin in ["U", "L"]:
        groupName = f"{skin}_SKIN"
        for i in range(2, 18, 2):
            bounds = ["SPAR.00", "SPAR.09", f"RIB.{i:02}", f"RIB.{i+2:02}"]
            FEASolver.addDVGroup(groupName, include=groupName, includeBounds=bounds)

        # Now add the skin panels inboard of the SOB, we can't add these the same way as above because there's no RIB.00,
        # addDVGroup will ignore any components already in other DVGroups so we only need the include argument
        FEASolver.addDVGroup(groupName, include=groupName)

    # rst end setup_tacs-skinDVs

    # Split stringers into three chordwise groups: front 3, middle 2, and back 3
    stringerGroups = [[1, 2, 3], [4, 5], [6, 7, 8]]

    # For both skins, go through the three stringer groups we just defined and split each one into 9 spanwise groups,
    # similar to the way we just did for the skins
    for skin in ["U", "L"]:
        for g in stringerGroups:
            group = [f"{skin}_STRING.{i:02}" for i in g]
            for i in range(2, 18, 2):
                bounds = ["SPAR.00", "SPAR.09", f"RIB.{i:02}", f"RIB.{i+2:02}"]
                FEASolver.addDVGroup("STRINGERS", include=group, includeBounds=bounds)
            FEASolver.addDVGroup("STRINGERS", include=group)

    # rst end setup DV

    # ==============================================================================
    #       Set-up constitutive properties for each DVGroup
    # ==============================================================================
    def conCallBack(dvNum, compDescripts, userDescript, specialDVs, **kargs):

        # Define Aluminium material properties and shell thickness limits
        rho_2024 = 2780  # Density, kg/m^3
        E_2024 = 73.1e9  # Elastic Modulus, Pa
        ys_2024 = 324e6  # Yield Strength, Pa
        nu = 0.33  # Poisson's ratio
        kcorr = 5.0 / 6.0  # Shear correction factor for isotropic shells

        # Set shell thickness depending on component type
        if "SKIN" in userDescript:
            t = 0.015
            tMin = 0.002
            tMax = 0.10
        elif "SPAR" in userDescript:
            tMin = 0.004
            tMax = 0.10
            if any(["SPAR.00" in d for d in compDescripts]):
                t = 0.014
            else:
                t = 0.01
        elif "STRINGER" in userDescript:
            t = 0.012
            tMin = 0.002
            tMax = 0.02
        elif "RIB" in userDescript:
            t = 0.004
            tMin = 0.002
            tMax = 0.10
        else:
            raise Exception(
                f"Oops, you didn't define a thickness for this kind of component (userDescript: {userDescript}) :("
            )

        # Create constitutive object
        con = constitutive.isoFSDTStiffness(rho_2024, E_2024, nu, kcorr, ys_2024, t, dvNum, tMin, tMax)
        scale = [100.0]
        return con, scale

    # rst end conCallBack

    # TACS will now create the constitutive objects for the different DV groups
    FEASolver.createTACSAssembler(conCallBack)

    # Write out components to visualize design variables (contour of dv1)
    FEASolver.writeDVVisualization(os.path.join(output, "dv_visual.f5"))

    # rst end createAssembler

    # ==============================================================================
    #       Add functions
    # ==============================================================================

    # Mass functions
    FEASolver.addFunction("TotalMass", functions.StructuralMass)
    FEASolver.addFunction("mass", functions.StructuralMass)
    FEASolver.addFunction("uSkin", functions.StructuralMass, include="U_SKIN")
    FEASolver.addFunction("lSkin", functions.StructuralMass, include="L_SKIN")
    FEASolver.addFunction("leSpar", functions.StructuralMass, include=["SPAR.00"])
    FEASolver.addFunction("teSpar", functions.StructuralMass, include=["SPAR.09"])
    FEASolver.addFunction("ribs", functions.StructuralMass, include=["RIBS"])

    funcGroups = {"USkin": ["U_SKIN", "U_STRING"], "LSkin": ["L_SKIN", "L_STRING"], "Spars_Ribs": ["SPARS", "RIBS"]}

    safetyFactor = 1.5
    KSWeight = 80.0

    # Add a max failure and KS failure function for each component group.
    for name, comps in funcGroups.items():
        FEASolver.addFunction(name + "Mass", functions.StructuralMass, include=comps)
        FEASolver.addFunction(
            name + "MaxFailure", functions.AverageMaxFailure, include=comps, safetyFactor=safetyFactor
        )
        # KS aggregated von Mises stress functions
        FEASolver.addFunction(
            name + "KSFailure", functions.AverageKSFailure, include=comps, KSWeight=KSWeight, safetyFactor=safetyFactor
        )

    return FEASolver
