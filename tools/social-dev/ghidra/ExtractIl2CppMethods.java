// Extracts decompiled IL2CPP method bodies for a small, explicitly named set of
// methods. Run as a Ghidra postScript with arguments:
//   <output-file> <method-name>=<rva> ...
//
// The RVA values come from Il2CppDumper's script.json. The script deliberately
// keeps the target list explicit so a review package cannot silently become a
// whole-binary dump.

import java.io.File;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.Arrays;

import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;

public class ExtractIl2CppMethods extends GhidraScript {

    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length < 2) {
            println("Usage: <output-file> <method-name>=<rva> ...");
            return;
        }

        File output = new File(args[0]);
        File parent = output.getParentFile();
        if (parent != null) {
            parent.mkdirs();
        }

        DecompInterface decompiler = new DecompInterface();
        decompiler.setSimplificationStyle("decompile");
        if (!decompiler.openProgram(currentProgram)) {
            throw new RuntimeException("Unable to open program in decompiler");
        }

        try (PrintWriter writer = new PrintWriter(new FileWriter(output))) {
            writer.println("# program=" + currentProgram.getName());
            writer.println("# image_base=" + currentProgram.getImageBase());
            writer.println("# targets=" + Arrays.toString(Arrays.copyOfRange(args, 1, args.length)));

            for (int i = 1; i < args.length;) {
                String target = args[i];
                String name;
                long rva;
                int split = target.lastIndexOf('=');
                if (split > 0 && split < target.length() - 1) {
                    name = target.substring(0, split);
                    rva = Long.parseLong(target.substring(split + 1));
                    i++;
                } else if (i + 1 < args.length) {
                    // Ghidra's headless argument parser may split a literal
                    // "name=rva" into two script arguments on Windows.
                    name = target;
                    rva = Long.parseLong(args[i + 1]);
                    i += 2;
                } else {
                    writer.println("\n===== INVALID TARGET " + target + " =====");
                    break;
                }

                Address address = currentProgram.getImageBase().add(rva);
                Function function = getFunctionAt(address);
                if (function == null) {
                    function = createFunction(address, name.replace('.', '_').replace('$', '_'));
                }

                writer.println("\n===== " + name + " RVA=0x" + Long.toHexString(rva)
                        + " ADDRESS=" + address + " =====");
                if (function == null) {
                    writer.println("<function-not-found>");
                    continue;
                }

                DecompileResults result = decompiler.decompileFunction(function, 180, monitor);
                if (!result.decompileCompleted()) {
                    writer.println("<decompile-failed> " + result.getErrorMessage());
                    continue;
                }
                writer.println(result.getDecompiledFunction().getC());
            }
        } finally {
            decompiler.dispose();
        }
    }
}
