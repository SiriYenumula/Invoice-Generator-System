import streamlit as st
from reportlab.pdfgen import canvas

st.title("Invoice Generator System")

# Session variables
if "page" not in st.session_state:
    st.session_state.page = "home"


# ---------------- HOME PAGE ----------------

if st.session_state.page == "home":

    st.header("Welcome")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Login"):
            st.session_state.page = "login"
            st.rerun()

    with col2:
        if st.button("Sign Up"):
            st.session_state.page = "signup"
            st.rerun()


# ---------------- LOGIN PAGE ----------------

# LOGIN
elif st.session_state.page == "login":
    st.header("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login Now"):

        if username == "":
            st.error("Please enter username")

        elif password == "":
            st.error("Please enter password")

        else:
            login_success = False

            with open("users.txt", "r") as file:
                users = file.readlines()

            for user in users:
                stored_username, stored_password = user.strip().split(",")

                if stored_username == username and stored_password == password:
                    login_success = True
                    break

            if login_success:
                st.session_state.login_success = True
            else:
                st.error("Invalid username or password")

    if st.session_state.get("login_success", False):
        st.success("Login successful")

        if st.button("Continue"):
            st.session_state.page = "invoice"
            st.session_state.login_success = False
            st.rerun()

# ---------------- SIGNUP PAGE ----------------

elif st.session_state.page == "signup":

    st.header("Sign Up")

    username = st.text_input("New Username")
    password = st.text_input("New Password", type="password")

    if st.button("Sign Up Now"):

        if username == "":
            st.error("Please enter username")

        elif password == "":
            st.error("Please enter password")

        else:

            with open("users.txt", "r") as file:
                users = file.readlines()

            username_exists = False

            for user in users:

                stored_username = user.strip().split(",")[0]

                if stored_username == username:
                    username_exists = True
                    break

            if username_exists:

                st.error("Username already exists")

            else:

                with open("users.txt", "a") as file:
                    file.write(username + "," + password + "\n")

                st.success("Signup successful")


# ---------------- INVOICE PAGE ----------------

elif st.session_state.page == "invoice":

    st.header("Invoice")

    # Logout button
    if st.button("Logout"):
        st.session_state.page = "home"
        st.rerun()

    # New Invoice button
    if st.button("New Invoice"):
        st.session_state.company_name = ""
        st.session_state.customer_name = ""
        st.session_state.product = ""
        st.session_state.quantity = 1
        st.session_state.price = 0.0
        st.session_state.gst = 0.0
        st.rerun()

    # Invoice input fields
    st.subheader("Company & Customer Details")

    company_name = st.text_input("Company Name", key="company_name")
    customer_name = st.text_input("Customer Name", key="customer_name")

    st.subheader("Product Details")

    product = st.text_input("Product", key="product")
    quantity = st.number_input("Quantity", min_value=1, key="quantity")
    price = st.number_input("Price", min_value=0.0, key="price")
    gst = st.number_input("GST (%)", min_value=0.0, key="gst")

    # Generate Invoice button
    if st.button("Generate Invoice"):
        if company_name == "":
            st.error("Please enter company name")

        elif customer_name == "":
            st.error("Please enter customer name")

        elif product == "":
            st.error("Please enter product name")

        elif price <= 0:
            st.error("Please enter a valid price")


        else:

            # Calculate amounts
            subtotal = quantity * price

            gst_amount = subtotal * gst / 100

            total = subtotal + gst_amount

            # Display amounts
            st.write("Subtotal:", subtotal)

            st.write("GST Amount:", gst_amount)

            st.write("Total:", total)

            # Save invoice to text file
            with open("invoices.txt", "a") as file:
                file.write(
                    company_name + "," +
                    customer_name + "," +
                    product + "," +
                    str(quantity) + "," +
                    str(price) + "," +
                    str(gst) + "," +
                    str(total) + "\n"
                )

            st.success("Invoice saved successfully")

            # ---------------- CREATE PDF ----------------

            pdf_file = "invoice.pdf"

            c = canvas.Canvas(pdf_file)

            # Invoice heading
            c.setFont("Helvetica-Bold", 20)
            c.drawCentredString(300, 800, "INVOICE")

            # Company and customer details
            c.setFont("Helvetica", 12)
            c.drawString(50,750,"Company Name: " + company_name)

            c.drawString(50,730,"Customer Name: " + customer_name)

            # Line
            c.line(50, 710, 550, 710)

            # Product details heading
            c.setFont("Helvetica-Bold", 14)
            c.drawString( 50,680,"Product Details")

            # Product information
            c.setFont("Helvetica", 12)

            c.drawString( 50, 650, "Product: " + product)

            c.drawString(50,630,"Quantity: " + str(quantity))

            c.drawString(50,610,"Price: ₹" + str(price))

            # Line
            c.line(50, 590, 550, 590)

            # Amount details
            c.setFont("Helvetica-Bold", 14)

            c.drawString( 50,560,"Amount Details")

            c.setFont("Helvetica", 12)

            c.drawString(50,530, "Subtotal: ₹" + str(subtotal))

            c.drawString(50, 510,"GST: " + str(gst) + "%")

            c.drawString(50,490,"GST Amount: ₹" + str(gst_amount))

            # Total
            c.setFont("Helvetica-Bold", 14)

            c.drawString( 50, 450,"Total Amount: ₹" + str(total))

            # Closing
            c.setFont("Helvetica", 12)

            c.drawString(50,400,"Thank you for your business!")

            # Save PDF
            c.save()

            st.success("PDF generated successfully")

            # ---------------- DOWNLOAD PDF ----------------

            with open(pdf_file, "rb") as file:
                pdf_data = file.read()

            st.download_button(
                label="Download Invoice",
                data=pdf_data,
                file_name="invoice.pdf",
                mime="application/pdf"
            )

            # View Saved Invoices button
            #if st.button("View Saved Invoices"):
                #st.session_state.page = "saved_invoices"
                #st.rerun()

    if st.button("View Saved Invoices"):
        st.session_state.page = "saved_invoices"
        st.rerun()
# ---------------- SAVED INVOICES PAGE ----------------

elif st.session_state.page == "saved_invoices":

    st.header("Saved Invoices")

    # Back to Invoice button
    if st.button("Back to Invoice"):
        st.session_state.page = "invoice"
        st.rerun()

    # Read invoices from text file
    with open("invoices.txt", "r") as file:
        invoices = file.readlines()

    st.write("Number of invoices:", len(invoices))

    if len(invoices) == 0:

        st.info("No saved invoices found.")

    else:

        # Display all invoices
        for number, invoice in enumerate(invoices, start=1):

            data = invoice.strip().split(",")

            st.subheader("Invoice " + str(number))

            with st.container(border=True):

                st.write("Company:",data[0])

                st.write("Customer:", data[1])

                st.write("Product:",data[2])

                st.write("Quantity:",data[3])

                st.write("Price: ₹", data[4])

                st.write( "GST:", data[5] + "%")

                st.write("Total: ₹",data[6])

            st.write("--------------------")